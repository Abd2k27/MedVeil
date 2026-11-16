"""Essai rapide d'EDS-Pseudo.

Sans argument : règles seules (aucun compte nécessaire).
Avec --modele : modèle public complet (demande l'accès Hugging Face + `hf auth login`).
"""
import sys
import edsnlp
from phrases_test import PHRASES

if "--modele" in sys.argv:
    nlp = edsnlp.load("AP-HP/eds-pseudo-public", auto_update=True)
else:
    nlp = edsnlp.blank("eds")
    nlp.add_pipe("eds.normalizer")
    nlp.add_pipe("eds_pseudo.simple_rules", config={"pattern_keys": ["TEL", "MAIL", "SECU", "PERSON"]})
    nlp.add_pipe("eds_pseudo.addresses")
    nlp.add_pipe("eds_pseudo.dates")

for phrase in PHRASES:
    print("\n>", phrase)
    for ent in nlp(phrase).ents:
        print(f"   {ent.label_:<16} {ent.text!r}")
