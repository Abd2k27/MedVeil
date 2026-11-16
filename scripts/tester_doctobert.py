"""Essai rapide de DoctoBERT : il complète un mot masqué (ce n'est pas encore un outil de pseudonymisation)."""
from transformers import AutoTokenizer, pipeline

MODELE = "doctolib-lab/doctobert-fr-base"
fill = pipeline("fill-mask", model=MODELE)
m = fill.tokenizer.mask_token

for phrase in [
    f"Le patient souffre d'une {m} aiguë.",
    f"Diabète de type 2 traité par {m} 1000 mg.",
    f"La patiente a été vue en consultation par le Dr {m}.",
]:
    print("\n>", phrase)
    for r in fill(phrase, top_k=5):
        print(f"   {r['token_str']!r:<20} {r['score']:.2f}")

print("\nDécoupage des noms en sous-mots :")
tok = AutoTokenizer.from_pretrained(MODELE)
for nom in ["Martin", "Dupont", "Benali", "Bouzid", "Adjovi", "Houngbédji", "Dossou-Yovo", "Kowalczyk"]:
    print(f"   {nom:<14} {tok.tokenize(nom)}")
