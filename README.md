# 🌾 AgroPredict SN - Prédiction des rendements agricoles par IA

**Aide les producteurs sénégalais à mieux anticiper les saisons grâce à l'IA et à la physique numérique.**

![Badge Python](https://img.shields.io/badge/Python-3.11-blue)
![Badge Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B)
![Badge XGBoost](https://img.shields.io/badge/XGBoost-2.0-green)
![Badge Senegal](https://img.shields.io/badge/Made%20for-Sénégal-00A651)

**Projet de fin d'études Master 2 Data Science & Génie Logiciel**  
**Auteur : Papa Malick NDIAYE**  
**Université : Alioune Diop de Bmabey**  

### Pourquoi ce projet ?
L'agriculture représente plus de 15% du PIB sénégalais. Avec le changement climatique, les rendements de l'arachide, du mil, du maïs et du riz deviennent de plus en plus imprévisibles.  
AgroPredict SN combine **modélisation physique** + **Machine Learning** pour prédire les rendements région par région et donner des recommandations concrètes aux agriculteurs et coopératives.

### Fonctionnalités
- Prédiction des rendements pour 5 cultures principales (arachide, mil, maïs, riz, sorgho)
- Carte interactive du Sénégal (14 régions)
- Simulation physique simplifiée de bilan hydrique
- Explicabilité des prédictions (SHAP)
- Recommandations : date de semis, variété, besoin en irrigation
- API prête à être utilisée par d'autres développeurs

### Architecture
AgroPredict_SN/
├── README.md                          # Documentation GitHub pro + visuelle
├── requirements.txt                   # Dépendances
├── .env.example                       # Variables d'environnement
├── Dockerfile                         # Déploiement facile
├── streamlit_app.py                   # Tableau de bord principal (multi-pages)
├── architecture.txt                   # Ce fichier
├── data/
│   ├── raw/
│   │   └── sample_yield_data.csv      # Données synthétiques réalistes (basées sur ANSD/FAO)
│   └── processed/                     # (généré automatiquement)
├── models/
│   ├── __init__.py
│   ├── train_model.py                 # Entraînement XGBoost + simulation physique simple
│   ├── predict.py                     # Prédictions + explicabilité SHAP
│   └── yield_model.pkl                # (généré après entraînement)
├── utils/
│   ├── __init__.py
│   ├── data_loader.py                 # Chargement et nettoyage
│   ├── preprocessing.py               # Préparation des features
│   └── visualization.py               # Graphiques et cartes
├── pages/                             # Pages Streamlit supplémentaires
│   ├── 1_Prediction_Rendements.py
│   ├── 2_Carte_Interactive.py
│   ├── 3_Recommandations.py
│   └── 4_About.py
├── notebooks/                         # (optionnel pour toi)
│   └── exploration.ipynb
├── tests/
│   └── test_model.py
└── .github/
    └── workflows/
        └── deploy.yml                 # GitHub Actions (optionnel)

### Comment l'utiliser ?
```bash
git clone https://github.com/pa-malick/AgroPredict_SN.git
cd AgroPredict_SN
pip install -r requirements.txt
streamlit run streamlit_app.py
