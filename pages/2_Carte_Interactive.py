import streamlit as st
import folium
from streamlit_folium import st_folium
from models.predict import predict_yield

st.title("🗺️ Carte Interactive du Sénégal")

# Paramètres (on reprend les mêmes que dans l'app principale)
crop = st.selectbox("Choisissez une culture", ["Arachide", "Mil", "Maïs", "Riz", "Sorgho"], key="map_crop")

rainfall = st.slider("Pluie cumulée (mm)", 300, 1200, 650, key="map_rain")
temp = st.slider("Température moyenne (°C)", 24.0, 32.0, 27.5, key="map_temp")
ndvi = st.slider("Indice NDVI", 0.4, 0.9, 0.65, key="map_ndvi")

if st.button("Afficher la carte des prédictions"):
    with st.spinner("Génération de la carte..."):
        # Simulation de prédictions pour plusieurs régions
        regions = ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda"]
        example_preds = {r: predict_yield(r, crop, rainfall, temp, ndvi) for r in regions}
        
        # Création de la carte
        m = folium.Map(location=[14.5, -14.5], zoom_start=6)
        
        regions_coords = {
            "Thiès": [14.79, -16.92],
            "Fatick": [14.35, -16.41],
            "Kaolack": [14.15, -15.91],
            "Saint-Louis": [16.02, -16.49],
            "Kaffrine": [14.10, -15.55],
            "Tambacounda": [13.77, -13.67]
        }
        
        for reg, coord in regions_coords.items():
            pred = example_preds.get(reg, 1.5)
            folium.Marker(
                location=coord,
                popup=f"<b>{reg}</b><br>Rendement : {pred:.2f} t/ha",
                icon=folium.Icon(color="green")
            ).add_to(m)
        
        # Affichage correct de la carte
        st_folium(m, width=800, height=600)
        