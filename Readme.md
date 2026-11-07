# MedVeil

> **MedVeil mesure et corrige les inégalités de protection dans la pseudonymisation des données de santé, de l'Europe à l'Afrique francophone.**

🚧 *Projet en démarrage : rien n'est encore implémenté.*

---

## Le problème

Les outils de pseudonymisation de textes médicaux en français (EDS-Pseudo, OpenMed…) sont entraînés surtout sur des noms, des adresses et des formats français. Or les hôpitaux européens soignent des patients de toutes origines.

Si un modèle repère « Jean Dupont » mais rate « Kossi Houngbédji » ou « Fatima Benali », ces patients sont **moins bien protégés** que les autres : leur nom fuit dans des données censées être anonymes.

- **C'est une faille RGPD.** Une donnée mal pseudonymisée reste une donnée personnelle.
- **C'est un biais algorithmique.** À notre connaissance, aucun projet existant ne le mesure.

**La question posée par MedVeil :** un outil d'anonymisation protège-t-il aussi bien un patient qui s'appelle Dupont qu'un patient qui s'appelle Houngbédji ?

---

## Ce que contient MedVeil

### 1. Un outil de pseudonymisation

Il prend un compte rendu médical, remplace les informations identifiantes par de fausses et laisse l'information médicale intacte.

| | |
|---|---|
| **Entrée** | Mme Kossiwa Adjovi, née le 12/03/1985, vue au CHU de Cotonou, tél. +229 97 12 34 56. Diabète de type 2, metformine 1000 mg. |
| **Sortie** | Mme Claire Martin, née le 04/07/1985, vue au CHU de Lyon, tél. 06 45 78 21 90. Diabète de type 2, metformine 1000 mg. |

Il repose sur un modèle **DoctoBERT** entraîné et combiné à des **règles**. On pourra l'utiliser comme bibliothèque Python et via une démo web.

### 2. Un banc d'essai de robustesse

Il se compose d'un jeu de comptes rendus et d'un script d'évaluation. N'importe quelle équipe (hôpital, éditeur, chercheur) pourra y faire passer son propre outil pour repérer ses angles morts.

**Méthode :**
1. Partir de comptes rendus réalistes, issus du corpus **PARHAF**.
2. Générer plusieurs versions **identiques** de chaque texte, où seuls les identifiants changent selon l'origine des noms : français, maghrébins, ouest-africains, est-européens, etc.
3. Faire passer chaque version dans les outils comparés.
4. Mesurer le **taux de détection par groupe**.

Le texte médical étant le même d'une version à l'autre, tout écart de performance vient uniquement des identifiants.

### 3. Des résultats

Ils prendront la forme de tableaux et d'un article court (arXiv ou blog technique) :

- « Les outils actuels détectent **X %** des noms d'origine française, mais seulement **Y %** des noms d'origine ouest-africaine. »
- « MedVeil réduit cet écart à **Z %**, sans perdre en performance sur les noms français. »

*(Valeurs à déterminer par les expériences.)*

---

## Systèmes comparés

| Système | Rôle |
|---|---|
| EDS-Pseudo | Référence à battre |
| OpenMed | Référence à battre |
| LLM (à définir) | Point de comparaison |
| DoctoBERT entraîné (MedVeil) | Notre modèle |

---

## Correction : comment MedVeil réduit l'écart

On entraîne DoctoBERT sur des **données synthétiques diversifiées** :
- des noms de multiples origines ;
- des formats africains : numéros en **+229**, **identifiant national béninois**, quartiers de **Cotonou**, établissements de santé locaux.

L'objectif est de **réduire l'écart entre groupes sans dégrader** les performances sur les noms français.

---

## Feuille de route

| Phase | Contenu |
|---|---|
| **1. Définir** | Schéma d'étiquettes (noms, dates, adresses, téléphones, identifiants…), formats africains compris (identifiant national, numéros +229…) |
| **2. Données** | Listes de noms par origine (sources publiques), adresses et formats variés ; textes de base issus de PARHAF |
| **3. Règles** | Règles de détection adaptées, y compris aux formats africains |
| **4. Modèles** | Entraînement de DoctoBERT ; mise en place d'EDS-Pseudo, d'OpenMed et d'un LLM pour la comparaison |
| **5. Évaluer** | Scores par groupe d'origine des noms : c'est l'analyse centrale du projet |
| **6. Présenter** | Publication du banc d'essai, du modèle, de la démo et de l'article |

---

## Principes de rigueur

- **On parle d'« origine des noms »**, jamais de l'origine ou de l'ethnicité des personnes : on teste des chaînes de caractères, pas des individus.
- **Les listes de noms sont construites avec soin.** Elles viennent de sources publiques documentées et présentent une diversité au sein de chaque groupe.
- **Aucune donnée patient réelle** n'est publiée dans ce dépôt.

---

## À qui ça sert

- **En Europe :** aux hôpitaux et aux entrepôts de données de santé, pour vérifier que leur anonymisation ne laisse personne de côté.
- **En Afrique francophone :** c'est une première brique pour réutiliser des données médicales dans le respect de la vie privée, en vue de futurs projets data santé au Bénin.

---

## Licence

*À définir.*
