"""Simulateur de rendement agricole, ecran unique concu pour un telephone.

Cinq questions que l'agriculteur sait renseigner, deux chiffres en reponse :
le rendement attendu et la recolte totale sur sa parcelle.
"""

import streamlit as st

from models.predict import get_model_info, get_model_metrics, load_model, simulate
from utils.referentiel import CULTURES, IRRIGATIONS, REGIONS, libelles, vers_canonique

st.set_page_config(page_title="AgroPredict SN", page_icon="🌾", layout="centered")


@st.cache_resource(show_spinner="Préparation du modèle au premier démarrage…")
def _preparer_modele():
    """Entraine le modele au premier lancement s'il n'est pas deja present.

    Sur un hebergement comme Streamlit Cloud, l'artefact construit par la CI
    n'est pas disponible. On le reconstruit alors une seule fois : les donnees
    et leur empreinte sont versionnees et l'entrainement est deterministe, le
    modele obtenu est donc identique a celui de la CI. En local et sous Docker,
    le modele existe deja et cette fonction ne fait rien.
    """
    if load_model() is None:
        from models.train_model import train_yield_model
        train_yield_model()


_preparer_modele()

# Mise en page resserree, lisible sur un petit ecran. Pas de couleur ajoutee :
# l'application suit le theme clair ou sombre choisi par l'utilisateur.
st.markdown("""
<style>
  .block-container { max-width: 620px; padding-top: 2.5rem; padding-bottom: 3rem; }
  [data-testid="stMetricValue"] { font-size: 2rem; }
  footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Niveaux d'engrais exprimes en langage courant plutot qu'en kg par hectare.
ENGRAIS = {
    "Aucun": 0,
    "Un peu": 25,
    "Comme d'habitude": 50,
    "Beaucoup": 100,
}

st.title("AgroPredict SN")
st.caption("Estimez votre récolte avant de semer")

# EF-4 : sans modele, l'application affiche un message clair plutot qu'une
# trace d'erreur. Le modele est construit par la CI, il n'est pas dans le depot.
if not get_model_info():
    st.error(
        "Le simulateur n'est pas disponible pour le moment. "
        "Le modèle de prévision n'a pas été chargé."
    )
    st.caption("Installation locale : `python data/pipelines/build_final_dataset.py` "
               "puis `python -m models.train_model`.")
    st.stop()

with st.form("simulation"):
    region = st.selectbox("Votre région", libelles(REGIONS))
    culture = st.selectbox("Ce que vous cultivez", libelles(CULTURES))
    surface = st.number_input("Surface cultivée (hectares)",
                              min_value=0.25, max_value=50.0, value=1.0, step=0.25)
    engrais = st.radio("Engrais utilisé", list(ENGRAIS), horizontal=True)
    irrigation = st.selectbox("Irrigation", libelles(IRRIGATIONS))

    lancer = st.form_submit_button("Estimer ma récolte", type="primary",
                                   use_container_width=True)

if lancer:
    resultat = simulate(
        region=vers_canonique(REGIONS, region),
        crop=vers_canonique(CULTURES, culture),
        surface_ha=surface,
        fertilizer_kg_ha=ENGRAIS[engrais],
        irrigation_type=vers_canonique(IRRIGATIONS, irrigation),
    )

    bas, haut = resultat["fourchette_t_ha"]

    st.divider()

    gauche, droite = st.columns(2)
    gauche.metric("Rendement attendu", f"{resultat['rendement_t_ha']:.2f} t/ha",
                  help=f"Fourchette probable : {bas:.2f} à {haut:.2f} t/ha")
    droite.metric(f"Récolte sur {surface:g} ha", f"{resultat['recolte_t']:.2f} t",
                  help="Une tonne représente environ 20 sacs de 50 kg")

    st.write(f"Soit environ **{resultat['recolte_sacs']} sacs** de 50 kg, "
             f"pour une fourchette de {bas:.2f} à {haut:.2f} t/ha.")

    # Comparaison utile seulement si l'agriculteur a declare mettre de l'engrais.
    gain = resultat["rendement_t_ha"] - resultat["rendement_sans_engrais"]
    if ENGRAIS[engrais] > 0 and gain > 0:
        sacs_gagnes = round(gain * surface * 20)
        st.info(f"L'engrais vous apporte environ **+{gain:.2f} t/ha**, "
                f"soit {sacs_gagnes} sacs de plus sur votre parcelle.")

    st.caption(
        "Estimation en conditions de campagne normales, à partir des statistiques "
        "agricoles nationales. Ce n'est pas une prévision datée : la récolte réelle "
        "dépend aussi de la pluie et des ravageurs de l'année."
    )

st.divider()

infos = get_model_info()
metriques = get_model_metrics()
if infos:
    st.caption(
        f"Modèle v{infos['version']} · commit {infos['commit']} · "
        f"erreur moyenne {metriques.get('mae', 'n/d')} t/ha · "
        f"{metriques.get('n_samples', 'n/d')} observations"
    )
st.caption("Papa Malick NDIAYE · M2 Data Science & Génie Logiciel · Université Alioune Diop de Bambey")
