# 🌾 AgroPredict SN - Prédiction des rendements agricoles par IA

**Aide les producteurs sénégalais à mieux anticiper les saisons grâce à l'IA et à la physique numérique.**

![Badge Python](https://img.shields.io/badge/Python-3.11-blue)
![Badge Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B)
![Badge XGBoost](https://img.shields.io/badge/XGBoost-2.0-green)
![Badge Senegal](https://img.shields.io/badge/Made%20for-Sénégal-00A651)

**Projet de fin d'études Master 2 Data Science & Génie Logiciel**  
**Auteur : Papa Malick NDIAYE**  
**Université : [à compléter]**  

### Pourquoi ce projet ?
L'agriculture représente plus de 15% du PIB sénégalais. Avec le changement climatique, les rendements de l'arachide, du mil, du maïs et du riz deviennent de plus en plus imprévisibles.  
AgroPredict SN combine **modélisation physique** (mes compétences en Physique Numérique) + **Machine Learning** pour prédire les rendements région par région et donner des recommandations concrètes aux agriculteurs et coopératives.

### Fonctionnalités
- Prédiction des rendements pour 5 cultures principales (arachide, mil, maïs, riz, sorgho)
- Carte interactive du Sénégal (14 régions)
- Simulation physique simplifiée de bilan hydrique
- Explicabilité des prédictions (SHAP)
- Recommandations : date de semis, variété, besoin en irrigation
- API prête à être utilisée par d'autres développeurs

### Démo en ligne
*(Ajoute le lien Streamlit Sharing ou Hugging Face ici une fois déployé)*

### Comment l'utiliser ?
```bash
git clone https://github.com/tonusername/AgroPredict_SN.git
cd AgroPredict_SN
pip install -r requirements.txt
streamlit run streamlit_app.py