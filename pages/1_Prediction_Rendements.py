import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from models.predict import predict_interval, get_model_metrics, predict_yield
from utils.theme import inject_theme, page_header

st.set_page_config(page_title="Prédiction · AgroPredict SN", layout="wide")
inject_theme(active_page="Prediction_Rendements")

page_header("Prédiction des rendements", "Simulation par culture, région et conditions climatiques")

REGIONS = ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sédhiou"]
CROPS   = ["Arachide", "Mil", "Maïs", "Riz", "Sorgho"]
SOILS   = ["Sableux", "Argileux", "Latérite", "Sablo-argileux"]

col_form, col_result = st.columns([1, 2], gap="large")

with col_form:
    st.markdown('<div class="glass-card fade-in" style="padding:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:1rem;">Paramètres</div>', unsafe_allow_html=True)

    region   = st.selectbox("Région", REGIONS)
    crop     = st.selectbox("Culture", CROPS)
    soil     = st.selectbox("Type de sol", SOILS)
    irrig    = st.selectbox("Irrigation", ["Pluviale", "Aspersion", "Goutte-a-goutte", "Submersion"])
    rainfall = st.slider("Pluie saisonnière (mm)", 200, 1200, 650)
    temp     = st.slider("Température (°C)", 24.0, 33.0, 27.5, step=0.1)
    ndvi     = st.slider("Indice NDVI", 0.30, 0.92, 0.65, step=0.01)

    with st.expander("Paramètres avancés"):
        fertilizer = st.slider("Engrais (kg/ha)", 0, 200, 50, step=5)
        ph         = st.slider("pH du sol", 4.5, 7.8, 6.2, step=0.1)
        humidity   = st.slider("Humidité (%)", 30, 95, 62)
        pest       = st.slider("Pression ravageurs (0-1)", 0.0, 1.0, 0.10, step=0.05)

    st.markdown("</div>", unsafe_allow_html=True)
    predict_btn = st.button("Prédire le rendement", type="primary", use_container_width=True)

with col_result:
    if predict_btn:
        with st.spinner("Calcul XGBoost en cours..."):
            pred, low, high = predict_interval(
                region, crop, rainfall, temp, ndvi, soil,
                fertilizer_kg_ha=fertilizer, irrigation_type=irrig,
                humidity_pct=humidity, pest_pressure=pest, soil_ph=ph,
            )
            metrics = get_model_metrics()

        st.markdown(f"""
        <div class="glass-card fade-in" style="border-color:rgba(0,200,100,0.45);margin-bottom:1.2rem;">
            <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;">
                {crop} · {region} · {soil}
            </div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:4rem;font-weight:800;color:#00C851;line-height:1;">
                {pred:.2f}
                <span style="font-size:1.2rem;color:#7A9BB5;font-weight:400;"> t/ha</span>
            </div>
            <div style="color:#7A9BB5;font-size:0.85rem;margin-top:0.4rem;">
                Intervalle de confiance 95 % :
                <span style="color:#C8D8E8;font-weight:600;">{max(0,low):.2f} – {high:.2f} t/ha</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred,
                number={"suffix": " t/ha", "font": {"size": 28, "color": "#E8EDF2", "family": "Space Grotesk"}},
                gauge={
                    "axis": {"range": [0, 6], "tickcolor": "#7A9BB5", "tickfont": {"color": "#7A9BB5", "size": 11}},
                    "bar": {"color": "#00C851", "thickness": 0.25},
                    "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
                    "steps": [
                        {"range": [0, 1.0], "color": "rgba(255,60,60,0.15)"},
                        {"range": [1.0, 2.0], "color": "rgba(255,160,0,0.12)"},
                        {"range": [2.0, 6.0], "color": "rgba(0,200,100,0.10)"},
                    ],
                    "threshold": {"line": {"color": "#00FF77", "width": 3}, "value": pred},
                },
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=220,
                margin=dict(t=20, b=0, l=20, r=20), font_color="#C8D8E8",
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with c2:
            all_preds = {r: predict_yield(r, crop, rainfall, temp, ndvi, soil,
                         fertilizer_kg_ha=fertilizer, irrigation_type=irrig,
                         humidity_pct=humidity, pest_pressure=pest, soil_ph=ph) for r in REGIONS}
            df_comp = pd.DataFrame(list(all_preds.items()), columns=["Région", "Rendement"])
            df_comp = df_comp.sort_values("Rendement", ascending=True)
            df_comp["Color"] = ["#00C851" if r == region else "#2A4A6A" for r in df_comp["Région"]]

            fig_bar = go.Figure(go.Bar(
                x=df_comp["Rendement"], y=df_comp["Région"], orientation="h",
                marker_color=df_comp["Color"],
                text=[f"{v:.2f}" for v in df_comp["Rendement"]],
                textposition="outside", textfont={"color": "#C8D8E8", "size": 11},
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=220, margin=dict(t=10, b=10, l=0, r=40),
                xaxis=dict(showgrid=False, color="#7A9BB5", title="t/ha"),
                yaxis=dict(gridcolor="rgba(0,200,100,0.05)", color="#C8D8E8"),
                font_color="#C8D8E8",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        if metrics:
            st.markdown(f"""
            <div style="font-size:0.75rem;color:#3A5A7A;margin-top:0.5rem;display:flex;gap:1.5rem;flex-wrap:wrap;">
                <span>Modèle : <b style="color:#7A9BB5;">XGBoost</b></span>
                <span>R² : <b style="color:#00C851;">{metrics.get('r2','N/D')}</b></span>
                <span>RMSE : <b style="color:#0096FF;">{metrics.get('rmse','N/D')} t/ha</b></span>
                <span>N : <b style="color:#FFD060;">{metrics.get('n_samples','N/D')} obs.</b></span>
                <span>Source : <b style="color:#D080FF;">FAOSTAT + NASA POWER</b></span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="height:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1rem;">
            <div style="font-size:3rem;opacity:0.3;">🌾</div>
            <div style="color:#3A5A7A;font-size:0.95rem;">Renseignez les paramètres et lancez la prédiction</div>
        </div>
        """, unsafe_allow_html=True)
