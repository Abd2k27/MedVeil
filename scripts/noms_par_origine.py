"""Listes de noms par origine pour le mini banc d'essai.

ATTENTION : listes exploratoires écrites à la main (40 noms + 40 prénoms par groupe).
Pour le vrai banc d'essai, il faudra des listes issues de sources publiques documentées.
On parle d'« origine des noms », jamais de l'origine des personnes.
"""

NOMS = {
    "francais": [
        "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Durand", "Leroy",
        "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "David", "Bertrand", "Roux",
        "Vincent", "Fournier", "Morel", "Girard", "André", "Lefèvre", "Mercier", "Dupont",
        "Lambert", "Bonnet", "François", "Legrand", "Garnier", "Faure", "Rousseau", "Guérin",
        "Muller", "Henry", "Roussel", "Perrin", "Morin", "Mathieu", "Gauthier", "Chevalier",
    ],
    "maghrebin": [
        "Benali", "Bouzid", "Belkacem", "Haddad", "Saïdi", "Mansouri", "Cherif", "Benamar",
        "Bouaziz", "Khelifi", "Boukhari", "Hamidi", "Zerrouki", "Meziane", "Rahmani", "Belhadj",
        "Amrani", "Toumi", "Brahimi", "Slimani", "Benslimane", "Ouali", "Daoudi", "Chaoui",
        "Lahlou", "Bennani", "Tazi", "Alaoui", "Berrada", "Trabelsi", "Gharbi", "Jaziri",
        "Mejri", "Hamdi", "Dridi", "Ayari", "Kaddour", "Messaoudi", "Yahiaoui", "Mokrani",
    ],
    "ouest_africain": [
        "Houngbédji", "Adjovi", "Dossou", "Hounkpatin", "Agbossou", "Ahouansou", "Gbaguidi", "Zinsou",
        "Kpadonou", "Akpovi", "Sossou", "Tossou", "Hounsou", "Adjanohoun", "Gnonlonfoun", "Houessou",
        "Quenum", "Amoussou", "Agbodjan", "Mensah", "Diallo", "Traoré", "Coulibaly", "Diop",
        "Ndiaye", "Keïta", "Konaté", "Ouédraogo", "Sawadogo", "Camara", "Cissé", "Touré",
        "Fofana", "Kouassi", "Kouamé", "N'Guessan", "Sangaré", "Dembélé", "Sissoko", "Gueye",
    ],
}

PRENOMS = {
    "francais": [
        "Jean", "Pierre", "Michel", "Philippe", "Alain", "Nicolas", "Christophe", "Daniel",
        "Patrick", "Julien", "Sébastien", "Louis", "Hugo", "Lucas", "Antoine", "Guillaume",
        "Olivier", "Éric", "Stéphane", "Mathieu", "Marie", "Nathalie", "Isabelle", "Sylvie",
        "Catherine", "Martine", "Christine", "Françoise", "Valérie", "Sandrine", "Stéphanie", "Céline",
        "Monique", "Sophie", "Camille", "Léa", "Chloé", "Claire", "Hélène", "Émilie",
    ],
    "maghrebin": [
        "Mohamed", "Ahmed", "Karim", "Rachid", "Youssef", "Mehdi", "Samir", "Nabil",
        "Abdelkader", "Mustapha", "Hicham", "Tarek", "Walid", "Sofiane", "Amine", "Yacine",
        "Omar", "Hamza", "Bilal", "Khaled", "Fatima", "Khadija", "Aïcha", "Nadia",
        "Samira", "Leïla", "Malika", "Zohra", "Yasmine", "Salima", "Naïma", "Hayat",
        "Soumia", "Amel", "Houria", "Rania", "Meriem", "Zineb", "Farida", "Latifa",
    ],
    "ouest_africain": [
        "Kossi", "Codjo", "Koffi", "Kokou", "Sèdjro", "Mahoussi", "Gbènakpon", "Yaovi",
        "Kouadio", "Mamadou", "Ibrahima", "Ousmane", "Moussa", "Seydou", "Boubacar", "Abdoulaye",
        "Cheikh", "Modou", "Souleymane", "Issouf", "Kossiwa", "Sènami", "Fifamè", "Afi",
        "Akouvi", "Ayaba", "Adjoua", "Akissi", "Amenan", "Aminata", "Fatoumata", "Mariama",
        "Aïssatou", "Kadiatou", "Oumou", "Awa", "Bintou", "Djénéba", "Ramatoulaye", "Salimata",
    ],
}

GROUPES = list(NOMS)
assert all(len(v) == 40 and len(set(v)) == 40 for d in (NOMS, PRENOMS) for v in d.values())
