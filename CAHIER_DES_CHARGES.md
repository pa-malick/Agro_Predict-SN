# Cahier des charges — AgroPredict SN (v2)

**Auteur :** Papa Malick NDIAYE — M2 Data Science & Génie Logiciel, Université Alioune Diop de Bambey
**Date :** juillet 2026

---

## 1. Le problème

Un agriculteur sénégalais décide en début de saison quoi semer, sur quelle surface, avec ou sans
engrais. Il prend cette décision sans aucun repère chiffré : il n'existe pas d'outil simple qui lui
dise ce qu'il peut raisonnablement attendre de sa parcelle.

AgroPredict SN est un **simulateur** qui répond à une seule question :

> « Pour ma culture, dans ma région, avec mes pratiques : quel rendement puis-je attendre ? »

---

## 2. Pour qui

**Utilisateur unique : l'agriculteur.**

Ce qu'il a : un téléphone, une connexion faible, peu de temps.
Ce qu'il connaît : sa région, sa culture, sa surface, s'il met de l'engrais, s'il irrigue.
Ce qu'il ne connaît pas : NDVI, pH du sol, pression ravageurs, pluviométrie saisonnière en mm.

Le conseiller agricole peut utiliser l'outil, mais il n'est pas la cible : l'interface est conçue
pour l'agriculteur, pas pour lui.

---

## 3. Ce que le système fait — et ne fait pas

### Il fait

L'utilisateur saisit **5 informations** :

| Entrée | Exemple |
|---|---|
| Région | Kaolack |
| Culture | Arachide |
| Surface | 2,5 ha |
| Engrais | Oui, ~50 kg/ha |
| Irrigation | Non (pluvial) |

Il obtient **2 chiffres** :

- le rendement attendu en **t/ha**, avec une fourchette ;
- la **récolte totale estimée**, en sacs ou en tonnes — le chiffre qui lui parle vraiment.

Plus une comparaison simple : « avec de l'engrais, tu passerais de 0,9 à 1,1 t/ha ».

### Il ne fait pas

Ces exclusions sont volontaires et assumées :

- **Pas de prévision datée.** Le système ne dit pas « ta récolte de 2027 ». Il donne un rendement
  attendu en conditions normales. Le modèle ne sait pas extrapoler dans le futur — le promettre
  serait mentir.
- **Pas d'effet météo.** Pluie, température et NDVI ne sont pas demandés et n'influencent pas le
  résultat (voir §4).
- **Pas de conseil agronomique personnalisé.** Le système donne un ordre de grandeur, pas une
  recommandation qui engagerait la campagne d'un producteur.
- **Pas de données parcellaires réelles.** Le système ne collecte rien sur l'utilisateur.

---

## 4. Les données — ce qu'elles sont vraiment

C'est le point le plus important du document, et il est écrit ici pour ne pas être découvert
ailleurs.

**Les rendements ne sont pas des mesures de terrain.** Ils sont construits ainsi :

1. FAOSTAT fournit le rendement **national** réel du Sénégal, par culture, de 2000 à 2022.
2. Ce rendement national est **désagrégé par région** avec des facteurs issus des publications
   DAPSA (Kaolack produit plus d'arachide que Saint-Louis, etc.).
3. Une variabilité parcellaire est ajoutée selon l'engrais, l'irrigation et la pression ravageurs.

**Conséquence à assumer :** le modèle apprend cette règle de désagrégation. Ses métriques mesurent
sa capacité à la retrouver, **pas** sa capacité à prédire un rendement réel observé. Aucun R²
annoncé dans ce projet ne doit être présenté comme une performance prédictive de terrain.

**Pourquoi ce choix :** il n'existe pas de jeu de données public de rendements parcellaires au
Sénégal. Le choix est donc entre des données construites et transparentes, ou pas de projet.

**Ce qui reste valide :** les ordres de grandeur par culture et par région sont ancrés sur des
statistiques officielles. L'outil dit correctement que le riz de Saint-Louis rend plus que le mil
de Sédhiou. C'est déjà utile.

---

## 5. Exigences techniques

### Fonctionnement

| # | Exigence |
|---|---|
| EF-1 | L'interface fonctionne sur un écran de téléphone, sans défilement horizontal |
| EF-2 | Une simulation complète tient en un écran : 5 champs, un bouton, un résultat |
| EF-3 | Le résultat s'affiche en moins de 3 secondes sur connexion lente |
| EF-4 | L'application reste utilisable si le modèle est indisponible (message clair, pas de page blanche) |
| EF-5 | Aucune donnée utilisateur n'est stockée |

### Industrialisation

| # | Exigence |
|---|---|
| ENF-1 | Le modèle est un **artefact versionné**, produit par la CI, jamais à la volée au démarrage de l'application |
| ENF-2 | Chaque modèle est reproductible depuis un couple (commit, empreinte du jeu de données) |
| ENF-3 | Un seul pipeline de données. Les sources sont versionnées ou téléchargées de façon reproductible |
| ENF-4 | Le retour à la version précédente se fait sans réentraînement |
| ENF-5 | La CI vérifie : style, tests, contrat d'entrée, seuil de métrique, démarrage du conteneur |
| ENF-6 | Aucun secret dans le dépôt |

---

## 6. Critères d'acceptation

Règle : **un critère qui ne peut pas devenir un test automatique n'entre pas dans ce document.**
Chaque ligne ci-dessous correspond à un test qui doit exister dans `tests/`.

| # | Critère | Test |
|---|---|---|
| CA-1 | Toute valeur proposée par l'interface est connue du modèle. Une valeur inconnue lève une erreur explicite — jamais une prédiction silencieuse. | Test de contrat interface ↔ modèle |
| CA-2 | Chaque entrée exposée à l'utilisateur a un effet mesurable et dans le bon sens sur le résultat. | Test de sensibilité par variable |
| CA-3 | Le modèle chargé expose sa version et l'empreinte des données d'entraînement. | Test sur l'artefact |
| CA-4 | Aucune métrique n'est écrite en dur dans le code ou la documentation ; toutes viennent de l'artefact. | Recherche de valeurs codées en dur |
| CA-5 | Les rendements simulés restent dans les plages agronomiques connues du Sénégal, par culture. | Test de plausibilité |
| CA-6 | La CI échoue si l'un des critères ci-dessus échoue. | Pipeline rouge vérifié |

---

## 7. Limites reconnues

Listées ici pour être présentées, pas découvertes.

1. Les rendements sont désagrégés, pas observés (§4).
2. Le modèle ne prédit pas une année future.
3. Les effets climatiques ne sont pas modélisés — c'est la principale piste d'évolution.
4. Sept régions et cinq cultures seulement.
5. Le simulateur donne un ordre de grandeur ; il ne remplace pas un conseiller agricole.

---

## 8. Ce qui définirait la réussite

Un agriculteur ouvre l'outil sur son téléphone, saisit cinq informations, obtient en trois secondes
une estimation de récolte cohérente avec ce que produit réellement sa région — et le projet est
capable de dire précisément **quelle version du modèle** a produit ce chiffre, et de revenir en
arrière si elle est mauvaise.
