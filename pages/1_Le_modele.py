"""Page technique : d'ou vient le chiffre affiche par le simulateur.

Toutes les valeurs de cette page sont lues dans l'artefact du modele. Aucune
metrique n'est ecrite en dur, conformement au critere CA-4 du cahier des charges.
"""

import pandas as pd
import streamlit as st

from models.predict import get_feature_importances, get_model_info, get_model_metrics

st.set_page_config(page_title="Le modèle · AgroPredict SN", layout="centered")

st.markdown("""
<style>
  .block-container { max-width: 720px; padding-top: 2.5rem; }
  footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.title("Le modèle et ses limites")

infos = get_model_info()
metriques = get_model_metrics()

if not infos:
    st.error("Modèle non chargé. Lancez : python -m models.train_model")
    st.stop()

st.subheader("Traçabilité")
st.write(
    f"Version **{infos['version']}**, construite depuis le commit `{infos['commit']}`. "
    f"Empreinte du jeu de données : `{(infos.get('empreinte_donnees') or 'absente')[:16]}…`"
)
st.caption("Ces trois éléments permettent de reconstruire exactement ce modèle.")

st.subheader("Performance mesurée")
c1, c2, c3 = st.columns(3)
c1.metric("Erreur moyenne", f"{metriques.get('mae', 'n/d')} t/ha")
c2.metric("Erreur quadratique", f"{metriques.get('rmse', 'n/d')} t/ha")
c3.metric("R²", metriques.get("r2", "n/d"))

st.caption(
    f"Mesuré sur {metriques.get('n_test', 'n/d')} observations de test, jamais vues pendant "
    f"l'entraînement ({metriques.get('n_train', 'n/d')} observations) ni pendant le réglage "
    f"du nombre d'arbres. Le découpage est fait par groupe année/région/culture, afin que "
    f"des parcelles issues d'une même situation ne se retrouvent pas des deux côtés."
)

st.subheader("Ce qui pèse le plus dans la prédiction")
importances = get_feature_importances(top_n=10)
if importances:
    noms = {
        "crop_": "Culture : ", "region_": "Région : ", "soil_type_": "Sol : ",
        "irrigation_type_": "Irrigation : ", "variety_": "Variété : ",
    }
    lignes = []
    for nom, valeur in importances:
        for prefixe, libelle in noms.items():
            if nom.startswith(prefixe):
                nom = nom.replace(prefixe, libelle)
                break
        lignes.append({"Variable": nom, "Poids": valeur})
    st.bar_chart(pd.DataFrame(lignes).set_index("Variable"), horizontal=True, height=320)
    st.caption("La culture et la région dominent, ce qui est attendu : elles déterminent "
               "l'ordre de grandeur du rendement.")

st.subheader("D'où viennent les données")
st.markdown("""
Les rendements ne sont pas des mesures de terrain. Ils sont construits en trois temps :

1. **FAOSTAT** fournit le rendement national réel du Sénégal, par culture, de 2000 à 2022.
2. Ce rendement national est **réparti entre les régions** à l'aide de facteurs issus des
   publications DAPSA.
3. Une variabilité entre parcelles est ajoutée selon l'engrais, l'irrigation et la pression
   des ravageurs.

La météo, elle, est réelle : elle provient de l'API NASA POWER, agrégée sur la saison
des pluies de juin à octobre.
""")

st.warning(
    "Le modèle apprend cette règle de répartition. Ses métriques mesurent sa capacité à la "
    "retrouver, pas sa capacité à prédire un rendement réellement observé sur une parcelle. "
    "Il n'existe pas de jeu de données public de rendements parcellaires au Sénégal."
)

st.subheader("Limites reconnues")
st.markdown("""
- Les rendements sont répartis à partir de statistiques nationales, pas observés.
- Le modèle ne prédit pas une année future : il donne un rendement en conditions normales.
- Les effets climatiques ne sont pas modélisés. C'est la principale piste d'évolution.
- Sept régions et cinq cultures seulement.
- Le simulateur donne un ordre de grandeur, il ne remplace pas un conseiller agricole.
""")
