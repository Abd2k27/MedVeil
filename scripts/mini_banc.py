"""Mini banc d'essai : les outils protègent-ils autant les noms selon leur origine ?

Méthode : on part des comptes rendus PARHAF annotés (positions des noms connues), on crée
des variantes où seuls les noms et prénoms changent, puis on mesure pour chaque outil la
part des noms entièrement masqués.

Usage :
    python mini_banc.py                 # split dev (101 documents)
    python mini_banc.py --limite 5      # essai rapide
    python mini_banc.py --outils eds_pseudo
"""
import argparse
import json
import random
import re
import zlib
from pathlib import Path

import pandas as pd

from noms_par_origine import GROUPES, NOMS, PRENOMS

RACINE = Path(__file__).parent.parent
ANNOT = RACINE / "data/PARHAF-pseudo-annotated/data"
SORTIE = RACINE / "data/mini_banc"

OUTILS = {
    "eds_pseudo": "AP-HP/eds-pseudo-public",
    "openmed_superclinical": "OpenMed/OpenMed-PII-French-SuperClinical-Large-434M-v1",
    "openmed_snowflake": "OpenMed/OpenMed-PII-French-SnowflakeMed-Large-568M-v1",
}
VARIANTES = ["original"] + GROUPES
PREFIXE = re.compile(
    r"^(?:(?:Monsieur|Madame|Mademoiselle|Docteur|Professeur|Mme|Mlle|Mr|Dr|Pr|M)\.?\s+|[dDlL]['’])"
)


# ---------------------------------------------------------------- données
def charger(split):
    meta = pd.read_parquet(ANNOT / f"document_metadata/document_metadata_{split}.parquet")
    spans = pd.read_parquet(ANNOT / f"spans/spans_{split}.parquet")
    return meta.set_index("report").full_text.to_dict(), spans


def spans_de_noms(texte, spans_doc):
    """Renvoie les noms à remplacer : (début, fin, catégorie, rôle), sans civilité, sans chevauchement."""
    noms = []
    for s in spans_doc.itertuples():
        if s.attribute_Categorie not in ("FIRST_NAME", "LAST_NAME"):
            continue
        brut = texte[s.begin:s.end]
        m = PREFIXE.match(brut)
        debut = s.begin + (m.end() if m else 0)
        coeur = texte[debut:s.end]
        if sum(c.isalpha() for c in coeur) < 3 or "Nom de" in brut:
            continue  # initiales et annotations atypiques : ni remplacées ni notées
        noms.append((debut, s.end, s.attribute_Categorie, s.attribute_RolePER))
    noms.sort()
    sans_chevauchement = []
    for n in noms:
        if not sans_chevauchement or n[0] >= sans_chevauchement[-1][1]:
            sans_chevauchement.append(n)
    return sans_chevauchement


def construire_variante(report, texte, noms, groupe):
    """Remplace chaque nom par un nom du groupe. Même personne -> même remplaçant dans le document."""
    if groupe == "original":
        return texte, [dict(debut=d, fin=f, cat=c, role=r, nom=texte[d:f]) for d, f, c, r in noms]
    rng = random.Random(zlib.crc32(report.encode()))  # même tirage pour tous les groupes
    ordre = {cat: rng.sample(range(40), 40) for cat in ("FIRST_NAME", "LAST_NAME")}
    listes = {"FIRST_NAME": PRENOMS[groupe], "LAST_NAME": NOMS[groupe]}
    attribue, morceaux, or_, curseur, decalage = {}, [], [], 0, 0
    for d, f, cat, role in noms:
        original = texte[d:f]
        cle = (cat, original.lower())
        if cle not in attribue:
            n_deja = sum(1 for k in attribue if k[0] == cat)
            attribue[cle] = listes[cat][ordre[cat][n_deja % 40]]
        nouveau = attribue[cle].upper() if original.isupper() else attribue[cle]
        morceaux += [texte[curseur:d], nouveau]
        nd = d + decalage
        or_.append(dict(debut=nd, fin=nd + len(nouveau), cat=cat, role=role, nom=nouveau))
        decalage += len(nouveau) - (f - d)
        curseur = f
    morceaux.append(texte[curseur:])
    return "".join(morceaux), or_


# ---------------------------------------------------------------- outils
def predire(outil, textes):
    """textes : {cle: texte} -> {cle: [(début, fin, étiquette)]}"""
    if outil == "eds_pseudo":
        import edsnlp

        nlp = edsnlp.load(OUTILS[outil], auto_update=True)
        return {
            k: [(e.start_char, e.end_char, e.label_) for e in nlp(t).ents] for k, t in textes.items()
        }
    import torch
    from transformers import AutoTokenizer, pipeline

    tok = AutoTokenizer.from_pretrained(OUTILS[outil])
    tok.model_max_length = 512  # découpe les longs comptes rendus en fenêtres qui se recouvrent
    ner = pipeline(
        "ner",
        model=OUTILS[outil],
        tokenizer=tok,
        aggregation_strategy="simple",
        stride=128,
        device="mps" if torch.backends.mps.is_available() else -1,
    )
    preds = {}
    for i, (k, t) in enumerate(textes.items()):
        preds[k] = [(int(e["start"]), int(e["end"]), e["entity_group"]) for e in ner(t)]
        if i % 50 == 0:
            print(f"  {outil} : {i}/{len(textes)}", flush=True)
    return preds


# ---------------------------------------------------------------- mesure
def masque(texte, preds):
    m = [False] * len(texte)
    for d, f, _ in preds:
        for i in range(max(d, 0), min(f, len(texte))):
            m[i] = True
    return m


def couverture(texte, m, d, f):
    utiles = [i for i in range(d, f) if texte[i].isalnum()]
    return sum(m[i] for i in utiles) / len(utiles) if utiles else 1.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev")
    ap.add_argument("--limite", type=int)
    ap.add_argument("--outils", nargs="+", default=list(OUTILS))
    args = ap.parse_args()

    textes_src, spans = charger(args.split)
    reports = sorted(textes_src)[: args.limite] if args.limite else sorted(textes_src)

    textes, or_noms = {}, {}
    for r in reports:
        noms = spans_de_noms(textes_src[r], spans[spans.report == r])
        for g in VARIANTES:
            t, o = construire_variante(r, textes_src[r], noms, g)
            textes[f"{g}|{r}"], or_noms[f"{g}|{r}"] = t, o
            p = SORTIE / "variantes" / g / f"{r}.txt"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(t, encoding="utf-8")
    print(f"{len(reports)} documents x {len(VARIANTES)} variantes, "
          f"{sum(len(o) for k, o in or_noms.items() if k.startswith('original|'))} noms par variante")

    lignes, autres = [], []
    (SORTIE / "predictions").mkdir(parents=True, exist_ok=True)
    for outil in args.outils:
        cache = SORTIE / "predictions" / f"{outil}_{args.split}_{len(reports)}.json"
        if cache.exists():
            preds = json.loads(cache.read_text())
        else:
            preds = predire(outil, textes)
            cache.write_text(json.dumps(preds))
        for cle, texte in textes.items():
            g, r = cle.split("|", 1)
            m = masque(texte, preds[cle])
            for o in or_noms[cle]:
                c = couverture(texte, m, o["debut"], o["fin"])
                etiq = sorted({e for d, f, e in preds[cle] if d < o["fin"] and f > o["debut"]})
                lignes.append(dict(
                    outil=outil, groupe=g, report=r, cat=o["cat"], role=o["role"], nom=o["nom"],
                    couverture=round(c, 3), etiquettes="+".join(etiq),
                    contexte=texte[max(0, o["debut"] - 45):o["fin"] + 25].replace("\n", " ⏎ "),
                ))
            if g == "original":  # autres catégories : seulement sur le texte d'origine
                sd = spans[spans.report == r]
                or_car = [False] * len(texte)
                for s in sd.itertuples():
                    for i in range(s.begin, s.end):
                        or_car[i] = True
                    if s.attribute_Categorie not in ("FIRST_NAME", "LAST_NAME"):
                        autres.append(dict(
                            outil=outil, cat=s.attribute_Categorie, texte=s.span_text,
                            couverture=round(couverture(texte, m, s.begin, s.end), 3),
                        ))
                n_masq = sum(m)
                autres.append(dict(outil=outil, cat="_SURMASQUAGE", texte=r,
                                   couverture=sum(a and not b for a, b in zip(m, or_car)) / max(n_masq, 1)))

    df = pd.DataFrame(lignes)
    df.to_csv(SORTIE / f"resultats_noms_{args.split}.csv", index=False)
    pd.DataFrame(autres).to_csv(SORTIE / f"resultats_autres_{args.split}.csv", index=False)
    df["entier"] = df.couverture >= 0.999
    df["rate"] = df.couverture <= 0.001
    pd.set_option("display.width", 200)
    print("\n% de noms entièrement masqués, par outil et origine des noms")
    print((df.pivot_table(index="outil", columns="groupe", values="entier") * 100).round(1)[VARIANTES])
    print("\n% de noms totalement ratés")
    print((df.pivot_table(index="outil", columns="groupe", values="rate") * 100).round(1)[VARIANTES])


if __name__ == "__main__":
    main()
