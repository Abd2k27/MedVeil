"""Extrait 40 comptes rendus de PARHAF (2 par spécialité) en fichiers texte lisibles."""
from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).parent.parent / "data/PARHAF/data/train-00000-of-00001.parquet"
SORTIE = Path(__file__).parent.parent / "data/extraits_parhaf"
PAR_SPECIALITE = 2

SORTIE.mkdir(parents=True, exist_ok=True)
patients = pd.read_parquet(SOURCE)
choisis = patients.groupby("specialty", group_keys=False).sample(n=PAR_SPECIALITE, random_state=42)

lignes = []
for i, (_, p) in enumerate(choisis.sort_values("specialty").iterrows(), start=1):
    docs = p.documents
    texte, type_doc, nb_mots = docs["text"][0], docs["type"][0], int(docs["word_count"][0])
    nom = f"{i:02d}_{p.specialty.lower().replace(' ', '_').replace('/', '-')}_{p.id}.txt"
    (SORTIE / nom).write_text(texte, encoding="utf-8")
    lignes.append(f"{nom}\t{p.specialty}\t{type_doc}\t{nb_mots} mots\t{len(docs['text'])} document(s) pour ce patient")

(SORTIE / "00_INDEX.tsv").write_text("fichier\tspécialité\ttype\ttaille\tdocuments du patient\n" + "\n".join(lignes) + "\n", encoding="utf-8")
print(f"{len(lignes)} comptes rendus écrits dans {SORTIE}")
