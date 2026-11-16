"""Essai rapide d'un modèle OpenMed (détection de données personnelles en français)."""
import sys
from transformers import pipeline
from phrases_test import PHRASES

MODELE = sys.argv[1] if len(sys.argv) > 1 else "OpenMed/OpenMed-PII-French-SuperClinical-Large-434M-v1"
ner = pipeline("ner", model=MODELE, aggregation_strategy="simple")

for phrase in PHRASES:
    print("\n>", phrase)
    for e in ner(phrase):
        print(f"   {e['entity_group']:<14} {phrase[e['start']:e['end']]!r:<28} {e['score']:.2f}")
