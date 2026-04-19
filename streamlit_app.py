import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.visualization import plot_yield_distribution, create_senegal_map
from utils.theme import inject_theme, render_hero, kpi_row
from models.predict import predict_yield, predict_interval, get_model_metrics
from streamlit_folium import st_folium

st.set_page_config(
    page_title="AgroPredict SN",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme(active_page="")

# Barre latérale : paramètres de simulation
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem;'>
        <div style='font-family:Space Grotesk,sans-serif;font-size:1.3rem;font-weight:700;color:#E8EDF2;'>
            🌾 AgroPredict <span style='color:#00C851;'>SN</span>
        </div>
        <div style='font-size:0.72rem;color:#7A9BB5;margin-top:0.2rem;'>Plateforme Agricole · Sénégal</div>
    </div>
    <hr style='border-color:rgba(0,200,100,0.15);margin:0.8rem 0;'/>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:0.8rem;'>Paramètres de simulation</div>", unsafe_allow_html=True)

    region = st.selectbox("Région", ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sédhiou"])
    crop   = st.selectbox("Culture", ["Arachide", "Mil", "Maïs", "Riz", "Sorgho"])
    rainfall = st.slider("Pluie saisonnière (mm)", 200, 1200, 650)
    temp     = st.slider("Température moyenne (°C)", 24.0, 33.0, 27.5, step=0.1)
    ndvi     = st.slider("Indice NDVI", 0.30, 0.92, 0.65, step=0.01)

    predict_btn = st.button("Lancer la prédiction", type="primary", use_container_width=True)

    st.markdown("<hr style='border-color:rgba(0,200,100,0.1);margin:1.2rem 0 0.5rem;'/>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem;color:#3A5A7A;text-align:center;'>Papa Malick NDIAYE · M2 Data Science</div>", unsafe_allow_html=True)

# Section hero : bannière d'accueil avec globe animé
render_hero()

# Ligne de métriques clés du modèle
metrics = get_model_metrics()
r2   = metrics.get("r2", "N/D")
rmse = metrics.get("rmse", "N/D")
n    = metrics.get("n_samples", "N/D")

kpi_row([
    ("Précision R²",       f"{r2}",       "#00C851"),
    ("RMSE (t/ha)",        f"{rmse}",     "#0096FF"),
    ("Observations",       f"{n}",        "#FFD060"),
    ("Régions couvertes",  "7",           "#D080FF"),
    ("Cultures modélisées","5",           "#FF7A50"),
])

st.markdown("<br/>", unsafe_allow_html=True)

# Affichage du résultat après clic sur le bouton
if predict_btn:
    with st.spinner("Calcul en cours..."):
        pred, low, high = predict_interval(region, crop, rainfall, temp, ndvi)

    st.markdown(f"""
    <div class="glass-card fade-in" style="border-color:rgba(0,200,100,0.4);margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;">Rendement prévu · {crop} · {region}</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:3.2rem;font-weight:800;color:#00C851;line-height:1.1;">{pred:.2f} <span style="font-size:1.2rem;color:#7A9BB5;">t/ha</span></div>
                <div style="color:#7A9BB5;font-size:0.85rem;margin-top:0.3rem;">Intervalle 95% : <span style="color:#E8EDF2;">{max(0,low):.2f} – {high:.2f} t/ha</span></div>
            </div>
            <div style="text-align:right;">
                <div style="background:rgba(0,200,100,0.08);border:1px solid rgba(0,200,100,0.25);border-radius:12px;padding:1rem 1.5rem;">
                    <div style="font-size:0.72rem;color:#7A9BB5;margin-bottom:0.3rem;">CONDITIONS</div>
                    <div style="color:#C8D8E8;font-size:0.85rem;">🌧 {rainfall} mm &nbsp;·&nbsp; 🌡 {temp}°C &nbsp;·&nbsp; 🌿 NDVI {ndvi}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Onglets principaux de la page d'accueil
tab1, tab2, tab3 = st.tabs(["📊  Données historiques", "🗺️  Carte des rendements", "ℹ️  À propos"])

with tab1:
    st.markdown("<div class='section-title fade-in'>Historique des rendements</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Données calibrées · FAOSTAT / DAPSA / NASA POWER · 2005–2023</div>", unsafe_allow_html=True)
    try:
        df = load_data()
        col_a, col_b = st.columns([2, 1])
        with col_a:
            fig = plot_yield_distribution(df)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(5,10,20,0.8)",
                font_color="#C8D8E8",
                title_font_color="#E8EDF2",
                xaxis=dict(gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5"),
                yaxis=dict(gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5"),
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            st.dataframe(
                df.head(15),
                use_container_width=True,
                hide_index=True,
            )
    except Exception as e:
        st.error(f"Erreur chargement données : {e}")

with tab2:
    st.markdown("<div class='section-title fade-in'>Carte des prédictions · Sénégal</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-sub'>Culture simulée : {crop} · Pluie : {rainfall} mm</div>", unsafe_allow_html=True)

    REGIONS_LIST = ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sédhiou"]
    preds = {r: predict_yield(r, crop, rainfall, temp, ndvi) for r in REGIONS_LIST}

    cols = st.columns(len(preds))
    colors = ["#00C851", "#0096FF", "#FFD060", "#D080FF", "#FF7A50", "#00D4FF", "#FF5090"]
    for col, (reg, val), color in zip(cols, preds.items(), colors):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:1rem 0.7rem;border-color:{color}40;">
                <div style="font-size:0.7rem;color:#7A9BB5;margin-bottom:0.3rem;">{reg}</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:{color};">{val:.2f}</div>
                <div style="font-size:0.7rem;color:#3A5A7A;">t/ha</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    m = create_senegal_map(preds)
    st_folium(m, width=None, height=480, use_container_width=True)

with tab3:
    st.markdown("""
    <div class="fade-in" style="max-width:760px;">
        <div class="section-title">À propos d'AgroPredict SN</div>
        <div class="section-sub">Intelligence artificielle au service de l'agriculture sénégalaise</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="glass-card fade-in">
            <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#00C851;margin-bottom:0.8rem;">Modélisation</div>
            <ul style="color:#C8D8E8;font-size:0.9rem;line-height:2;padding-left:1.2rem;margin:0;">
                <li>Algorithme XGBoost (Gradient Boosting)</li>
                <li>535 observations · 2005–2023</li>
                <li>7 régions agricoles · 5 cultures</li>
                <li>R² = 0.98 · RMSE = 0.13 t/ha</li>
                <li>Intervalle de confiance 95%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="glass-card fade-in-2">
            <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#0096FF;margin-bottom:0.8rem;">Sources de données</div>
            <ul style="color:#C8D8E8;font-size:0.9rem;line-height:2;padding-left:1.2rem;margin:0;">
                <li>FAOSTAT :rendements historiques</li>
                <li>NASA POWER API :météo par région</li>
                <li>DAPSA / ANSD :statistiques nationales</li>
                <li>CHIRPS :pluviométrie haute résolution</li>
                <li>Copernicus / MODIS :NDVI satellite</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card fade-in-3" style="margin-top:1rem;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;">
        <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#00C851,#0096FF);display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:700;color:#fff;font-family:'Space Grotesk',sans-serif;">PM</div>
        <div>
            <div style="font-family:'Space Grotesk',sans-serif;font-weight:600;color:#E8EDF2;">Papa Malick NDIAYE</div>
            <div style="color:#7A9BB5;font-size:0.85rem;">Master 2 · Data Science & Génie Logiciel</div>
            <div style="color:#00C851;font-size:0.8rem;margin-top:0.2rem;">njaymika@gmail.com</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
