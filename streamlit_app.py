import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.visualization import plot_yield_distribution, create_senegal_map
from models.predict import predict_yield

# ====================== CONFIGURATION ======================
st.set_page_config(
    page_title="AgroPredict SN",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 AgroPredict SN")
st.markdown("**Prédiction intelligente des rendements agricoles au Sénégal**  \n*Par Papa Malick NDIAYE – Master 2 Data Science & Génie Logiciel*")

# ====================== SIDEBAR ======================
st.sidebar.header("🔧 Paramètres de prédiction")

region = st.sidebar.selectbox(
    "Région",
    ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sédhiou"]
)

crop = st.sidebar.selectbox(
    "Culture",
    ["Arachide", "Mil", "Maïs", "Riz", "Sorgho"]
)

rainfall = st.sidebar.slider("Pluie cumulée attendue (mm)", 300, 1200, 650)
temp = st.sidebar.slider("Température moyenne (°C)", 24.0, 32.0, 27.5)
ndvi = st.sidebar.slider("Indice NDVI (végétation)", 0.4, 0.9, 0.65)

# ====================== PREDICTION ======================
if st.sidebar.button("🔮 Prédire le rendement", type="primary"):
    with st.spinner("Calcul de la prédiction en cours..."):
        pred = predict_yield(region, crop, rainfall, temp, ndvi)
        
        st.success(f"**Rendement prévu pour {crop} dans la région de {region} : {pred:.2f} tonnes/ha**")

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["📊 Données historiques", "🗺️ Carte interactive", "ℹ️ À propos"])

with tab1:
    try:
        df = load_data()
        st.dataframe(df.head(10), use_container_width=True)
        st.plotly_chart(plot_yield_distribution(df), use_container_width=True)
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")

with tab2:
    st.subheader("Carte des rendements prévus au Sénégal")
    # Simulation de prédictions pour plusieurs régions
    example_preds = {}
    for r in ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine"]:
        example_preds[r] = predict_yield(r, crop, rainfall, temp, ndvi)
    
    m = create_senegal_map(example_preds)
    
    # Import ici pour éviter les problèmes d'import global
    from streamlit_folium import st_folium
    st_folium(m, width=700, height=500)

with tab3:
    st.markdown("""
    ### À propos d'AgroPredict SN
    
    Ce projet combine **Physique Numérique** et **Data Science** pour aider les producteurs sénégalais à mieux anticiper leurs rendements.
    
    - Modèle : XGBoost  
    - Données : Inspirées des statistiques ANSD / DAPSA / FAO  
    - Objectif : Réduire les risques liés au changement climatique
    
    **Auteur : Papa Malick NDIAYE**
    """)