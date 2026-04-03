import plotly.express as px
import folium
from streamlit_folium import st_folium
import streamlit as st

def plot_yield_distribution(df):
    """Graphique des rendements par culture et région."""
    fig = px.box(df, 
                 x='crop', 
                 y='yield_ton_ha', 
                 color='region',
                 title="Distribution des rendements par culture et par région",
                 labels={"yield_ton_ha": "Rendement (tonnes/ha)"})
    return fig


def create_senegal_map(example_preds):
    """Crée une carte interactive simple du Sénégal."""
    # Centre sur le Sénégal
    m = folium.Map(location=[14.5, -14.5], zoom_start=6, tiles="CartoDB positron")
    
    # Quelques régions avec coordonnées approximatives
    regions_coords = {
        "Thiès": [14.79, -16.92],
        "Fatick": [14.35, -16.41],
        "Kaolack": [14.15, -15.91],
        "Saint-Louis": [16.02, -16.49],
        "Kaffrine": [14.10, -15.55],
        "Tambacounda": [13.77, -13.67],
        "Sédhiou": [12.82, -15.55]
    }
    
    for reg, coord in regions_coords.items():
        pred = example_preds.get(reg, "N/A")
        folium.Marker(
            location=coord,
            popup=f"<b>{reg}</b><br>Rendement prévu : {pred} t/ha",
            tooltip=reg,
            icon=folium.Icon(color="green", icon="leaf")
        ).add_to(m)
    
    return m