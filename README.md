# AgroPredict SN - Prédiction des rendements agricoles au Sénégal

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0-006400)](https://xgboost.readthedocs.io)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](/.github/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Projet Master 2 - Data Science & Génie Logiciel**  
> Auteur : **Papa Malick NDIAYE** - njaymika@gmail.com

---

## Présentation

L'agriculture représente **~15 % du PIB sénégalais** et fait vivre plus de 60 % de la population active. Face au changement climatique, les rendements de l'arachide, du mil, du maïs, du riz et du sorgho deviennent de plus en plus imprévisibles.

**AgroPredict SN** combine Machine Learning (XGBoost) et données satellitaires officielles pour permettre aux agriculteurs, conseillers et décideurs d'**anticiper les rendements avant la saison des pluies**, région par région.

---

## Performances du modèle

| Métrique | Valeur |
|---|---|
| R² (coefficient de détermination) | **0.990** |
| RMSE | **0.13 t/ha** |
| MAE | **0.10 t/ha** |
| Observations d'entraînement | **6 440** |
| Variables (features) | **64** |
| Algorithme | XGBoost Gradient Boosting |

---

## Sources de données officielles

| Source | Données | Accès |
|---|---|---|
| [FAOSTAT](https://www.fao.org/faostat) | Rendements nationaux Sénégal 2000–2022 par culture | Bulk download officiel |
| [NASA POWER API](https://power.larc.nasa.gov) | Météo réelle par région : pluie, temp, humidité, vent, ensoleillement | REST API gratuite |
| [DAPSA / ANSD](https://agriculture.gouv.sn) | Facteurs de régionalisation par région agricole | Publications officielles |

---

## Fonctionnalités

- **Prédiction** des rendements pour 5 cultures × 7 régions avec intervalle de confiance 95 %
- **26 variables** : climatiques (NASA POWER réelles), pédologiques, agronomiques, géographiques
- **Carte interactive** avec rendements prévus colorés par intensité
- **Recommandations dynamiques** : variété, calendrier de semis, irrigation, alertes ravageurs
- **Explainabilité** : importance des variables + courbes de sensibilité par paramètre
- **Historique** : tendances 2000–2023, heatmap région × culture, comparaison saison N vs N-1
- **Export CSV** de l'historique des prédictions
- **Globe 3D** animé avec localisation des régions agricoles

---

## Architecture technique

```
AgroPredict_SN/
├── streamlit_app.py              # Page d'accueil
├── pages/
│   ├── 1_Prediction_Rendements.py
│   ├── 2_Carte_Interactive.py
│   ├── 3_Recommandations.py
│   ├── 4_About.py
│   ├── 5_Analyse_SHAP.py
│   └── 6_Historique.py
├── models/
│   ├── train_model.py            # Entraînement XGBoost
│   └── predict.py                # Inférence + intervalle de confiance
├── data/
│   ├── raw/
│   │   ├── senegal_yield_data.csv     # Dataset final (6 440 lignes)
│   │   ├── faostat_raw.csv            # Données FAOSTAT brutes
│   │   └── nasa_power_monthly.json    # Données NASA POWER brutes
│   └── pipelines/
│       ├── fetch_nasa_power.py        # Fetch API NASA POWER
│       └── build_final_dataset.py     # Pipeline de construction
├── utils/
│   ├── theme.py                  # UI corporate dark + globe 3D
│   ├── preprocessing.py          # Encodage + features
│   ├── data_loader.py
│   └── visualization.py
├── tests/
│   ├── test_model.py             # 10 tests modèle
│   └── test_data.py              # 7 tests données
├── .github/workflows/
│   ├── ci.yml                    # Lint + tests + build Docker
│   └── deploy.yml                # Deploy automatique
├── Dockerfile
└── docker-compose.yml
```

---

## Installation

### Locale

```bash
git clone https://github.com/Pa-Malick/AgroPredict_SN.git
cd AgroPredict_SN
pip install -r requirements.txt

# Générer le dataset et entraîner le modèle
python data/pipelines/build_final_dataset.py
python -m models.train_model

# Lancer l'application
streamlit run streamlit_app.py
```

### Docker

```bash
docker-compose up --build
# Application disponible sur http://localhost:8501
```

---

## Pipeline de données

```bash
# 1. Récupérer les données NASA POWER réelles (API gratuite)
python data/pipelines/fetch_nasa_power.py

# 2. Construire le dataset final (FAOSTAT + NASA POWER)
python data/pipelines/build_final_dataset.py

# 3. Entraîner le modèle
python -m models.train_model

# 4. Lancer les tests (17 tests)
pytest tests/ -v
```

---

## DevOps

| Composant | Détail |
|---|---|
| CI - GitHub Actions | Lint (flake8) + pytest + build Docker à chaque push |
| CD - GitHub Actions | Entraînement auto + déploiement Streamlit Cloud sur push `master` |
| Containerisation | Dockerfile multi-stage + healthcheck |
| Tests | 17 tests (données + modèle) - couverture critique |

---

## Variables du dataset

| Catégorie | Variables |
|---|---|
| Temporelle | `year` |
| Géographique | `region`, `latitude`, `longitude`, `elevation_m` |
| Agronomique | `crop`, `variety`, `irrigation_type`, `fertilizer_kg_ha`, `cycle_days`, `area_ha` |
| Pédologique | `soil_type`, `soil_ph` |
| Climatique (NASA POWER) | `rainfall_mm`, `temp_avg_c`, `temp_min_c`, `temp_max_c`, `humidity_pct`, `wind_speed_ms`, `sunshine_hours` |
| Végétation | `ndvi_avg`, `ndvi_min`, `ndvi_max` |
| Stress biotique | `pest_pressure` |
| Cible | `yield_ton_ha` |
| Traçabilité | `yield_national_faostat`, `source` |

---

## Auteur

**Papa Malick NDIAYE**  
Master 2 Data Science & Génie Logiciel  
njaymika@gmail.com
