<p align="center">
  <img src="docs/logo.png" alt="AgroPredict SN" width="440">
</p>

<p align="center">
  Simulateur de rendement agricole pour les producteurs sénégalais.
</p>

<p align="center">
  <b>Simulateur : <a href="https://agropredict-sn.streamlit.app">agropredict-sn.streamlit.app</a></b>
  &nbsp;·&nbsp;
  <b>Présentation : <a href="https://pa-malick.github.io/Agro_Predict-SN/">pa-malick.github.io/Agro_Predict-SN</a></b>
</p>

> Projet Master 2 Data Science & Génie Logiciel
> Auteur : Papa Malick NDIAYE — Université Alioune Diop de Bambey

---

## En une phrase

Un agriculteur répond à 5 questions sur son téléphone, et l'application lui dit
combien il va récolter.

## Comment ça marche, en 3 temps

**1. Les données.** On part des rendements agricoles réels du Sénégal (FAOSTAT)
et de la météo réelle (NASA POWER). Un script assemble tout ça en un tableau :
région, culture, engrais, irrigation... et le rendement obtenu.

**2. L'apprentissage.** Un modèle (XGBoost) lit ce tableau et apprend les
régularités : le riz de Saint-Louis rend plus que le mil de Sédhiou, l'engrais
aide un peu, etc. On enregistre ce qu'il a appris dans un fichier.

**3. L'application.** L'agriculteur choisit sa région, sa culture, sa surface,
son engrais, son irrigation. Le modèle calcule, et l'écran affiche deux chiffres :
le rendement (t/ha) et la récolte totale (en sacs).

> Ce n'est pas un modèle qui prédit l'avenir. C'est un simulateur honnête,
> industrialisé proprement : données assumées, modèle traçable, tests qui
> protègent réellement.

---

## Ce que fait l'application

L'agriculteur renseigne cinq informations qu'il connaît : sa région, sa culture,
sa surface, son engrais et son mode d'irrigation. Il obtient en retour le
rendement attendu en tonnes par hectare et la récolte totale correspondante,
exprimée en sacs de 50 kg.

L'interface tient sur un seul écran de téléphone.

## Ce qu'elle ne fait pas

- Elle ne prédit pas une année précise. Elle donne un rendement en conditions de
  campagne normales.
- Elle ne modélise pas la météo de l'année en cours.
- Elle ne remplace pas un conseiller agricole.

Ces limites sont volontaires et détaillées dans [CAHIER_DES_CHARGES.md](CAHIER_DES_CHARGES.md).

---

## Origine des données

| Source | Ce qu'elle apporte |
|---|---|
| FAOSTAT | Rendements nationaux réels du Sénégal, par culture, 2000 à 2022 |
| NASA POWER | Météo réelle par région, agrégée sur la saison des pluies |
| DAPSA | Facteurs de répartition régionale des rendements |

**Les rendements par parcelle ne sont pas des mesures de terrain.** Ils sont
obtenus en répartissant les rendements nationaux FAOSTAT entre les régions, puis
en ajoutant une variabilité liée aux pratiques. Le modèle apprend donc cette
règle de répartition : ses métriques mesurent sa capacité à la retrouver, pas à
prédire un rendement réellement observé.

Ce choix est assumé : il n'existe pas de jeu de données public de rendements
parcellaires au Sénégal.

---

## Accès

- Simulateur en ligne, sans rien installer : https://agropredict-sn.streamlit.app
- Page de présentation : https://pa-malick.github.io/Agro_Predict-SN/
- En local, voir ci-dessous.

## Installation locale

```bash
git clone https://github.com/Pa-Malick/AgroPredict_SN.git
cd AgroPredict_SN
pip install -r requirements.txt

python data/pipelines/build_final_dataset.py   # construit le jeu de données
python -m models.train_model                   # entraîne et enregistre le modèle
streamlit run streamlit_app.py
```

Avec Docker :

```bash
GIT_COMMIT=$(git rev-parse --short HEAD) docker compose up --build
```

L'application est disponible sur http://localhost:8501

---

## Structure

```
streamlit_app.py           simulateur, écran unique
pages/1_Le_modele.py       page technique : traçabilité, métriques, limites
models/train_model.py      entraînement, découpage par groupe
models/predict.py          simulation et validation des entrées
utils/referentiel.py       source unique des valeurs autorisées
utils/preprocessing.py     encodage des variables
utils/data_loader.py       chargement et empreinte du jeu de données
data/pipelines/            récupération NASA POWER et construction du jeu de données
tests/                     critères d'acceptation CA-1 à CA-6
```

---

## Qualité

Chaque critère du cahier des charges correspond à un test automatisé. La CI
échoue si l'un d'eux échoue.

| Critère | Vérifie |
|---|---|
| CA-1 | Toute valeur de l'interface est connue du modèle, sinon erreur explicite |
| CA-2 | Chaque entrée exposée a un effet mesurable et dans le bon sens |
| CA-3 | Le modèle expose sa version, son commit et l'empreinte de ses données |
| CA-4 | Aucune métrique n'est écrite en dur dans le code ou la documentation |
| CA-5 | Les rendements restent dans les plages agronomiques connues |
| CA-6 | La CI échoue si l'un des critères ci-dessus échoue |

```bash
pytest tests/ -v
```

Les métriques du modèle ne sont pas reproduites ici volontairement : elles sont
lues dans l'artefact et affichées sur la page « Le modèle ».

---

## Traçabilité et retour arrière

Chaque modèle entraîné enregistre sa version, le commit dont il provient et
l'empreinte SHA256 du jeu de données utilisé. Ces trois éléments suffisent à le
reconstruire à l'identique.

Pour revenir à une version précédente, relancer le workflow `Deploy` en
indiquant le tag voulu. L'image correspondante contient déjà son modèle, aucun
réentraînement n'est nécessaire.

---

## Auteur

**Papa Malick NDIAYE**
Master 2 Data Science & Génie Logiciel — Université Alioune Diop de Bambey
njaymika@gmail.com

## Licence

MIT, voir [LICENSE](LICENSE).
