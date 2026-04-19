import streamlit as st
import numpy as np
import plotly.graph_objects as go
from models.predict import load_model, get_feature_importances
from utils.theme import inject_theme, page_header

st.set_page_config(page_title="Analyse SHAP · AgroPredict SN", layout="wide")
inject_theme(active_page="Analyse_SHAP")

page_header("Explicabilite du modele", "Comprendre pourquoi le modele predit tel rendement")

# Chargement du modele entraine
bundle = load_model()
if bundle is None:
    st.error("Modele non charge. Lancez : python -m models.train_model")
    st.stop()

model   = bundle["model"]
metrics = bundle.get("metrics", {})

tab1, tab2 = st.tabs(["📊  Importance des variables", "🔍  Impact par parametre"])

with tab1:
    st.markdown("<div class='section-title fade-in'>Variables les plus influentes</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Score F (gain) : contribution moyenne de chaque variable a la reduction d'erreur</div>", unsafe_allow_html=True)

    # Recuperation des importances depuis le modele XGBoost
    top_feats = get_feature_importances(top_n=20)
    if not top_feats:
        st.warning("Importances non disponibles.")
        st.stop()

    # Nettoyage des noms de variables pour l'affichage
    names = [
        f[0].replace("crop_", "Culture: ").replace("region_", "Region: ")
        .replace("irrigation_type_", "Irrigation: ").replace("variety_", "Variete: ")
        .replace("soil_type_", "Sol: ")
        for f in top_feats
    ]
    values = [f[1] for f in top_feats]
    max_v  = max(values)
    # Couleur proportionnelle a l'importance
    colors = [f"rgba(0,{int(100+155*v/max_v)},{int(80+30*v/max_v)},{0.6+0.4*v/max_v})" for v in values]

    fig = go.Figure(go.Bar(
        x=values[::-1], y=names[::-1],
        orientation="h",
        marker_color=colors[::-1],
        text=[f"{v:.4f}" for v in values[::-1]],
        textposition="outside",
        textfont={"color": "#C8D8E8", "size": 11},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=600, margin=dict(t=10, b=10, l=180, r=80),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", title="Importance (F-score)"),
        yaxis=dict(color="#C8D8E8", tickfont={"size": 11}),
        font_color="#C8D8E8",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Metriques de performance du modele
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R²", metrics.get("r2", "N/D"))
    c2.metric("RMSE (t/ha)", metrics.get("rmse", "N/D"))
    c3.metric("MAE (t/ha)",  metrics.get("mae", "N/D"))
    c4.metric("Observations", metrics.get("n_samples", "N/D"))

with tab2:
    st.markdown("<div class='section-title fade-in'>Sensibilite du rendement aux parametres</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Faites varier un parametre et observez l'effet sur le rendement predit</div>", unsafe_allow_html=True)

    from models.predict import predict_yield

    # Deux colonnes : formulaire a gauche, graphique a droite
    col_ctrl, col_plot = st.columns([1, 2])

    with col_ctrl:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        region   = st.selectbox("Region", ["Thies", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sedhiou"])
        crop     = st.selectbox("Culture", ["Arachide", "Mil", "Mais", "Riz", "Sorgho"])
        irrig    = st.selectbox("Irrigation", ["Pluviale", "Aspersion", "Goutte-a-goutte", "Submersion"])
        param    = st.selectbox("Parametre a faire varier", [
            "rainfall_mm", "temp_avg_c", "ndvi_avg",
            "fertilizer_kg_ha", "pest_pressure", "soil_ph",
        ])
        temp_fix     = st.slider("Temperature fixe (C)", 24.0, 33.0, 27.5, step=0.5)
        ndvi_fix     = st.slider("NDVI fixe", 0.30, 0.92, 0.60, step=0.05)
        rainfall_fix = st.slider("Pluie fixe (mm)", 200, 1200, 650, step=50)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_plot:
        RANGES = {
            "rainfall_mm":      np.linspace(150, 1200, 60),
            "temp_avg_c":       np.linspace(22, 35, 60),
            "ndvi_avg":         np.linspace(0.20, 0.95, 60),
            "fertilizer_kg_ha": np.linspace(0, 200, 60),
            "pest_pressure":    np.linspace(0, 1, 60),
            "soil_ph":          np.linspace(4.5, 7.8, 60),
        }
        LABELS = {
            "rainfall_mm": "Pluie saisonniere (mm)",
            "temp_avg_c":  "Temperature moyenne (C)",
            "ndvi_avg":    "Indice NDVI",
            "fertilizer_kg_ha": "Engrais (kg/ha)",
            "pest_pressure": "Pression ravageurs (0-1)",
            "soil_ph":     "pH du sol",
        }

        # Calcul du rendement pour chaque valeur de la plage du parametre choisi
        xs = RANGES[param]
        ys = []
        for v in xs:
            kw = {
                "region": region, "crop": crop,
                "rainfall_mm": rainfall_fix, "temp_avg_c": temp_fix,
                "ndvi_avg": ndvi_fix, "irrigation_type": irrig,
            }
            kw[param] = float(v)
            ys.append(predict_yield(**kw))

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=xs, y=ys,
            mode="lines",
            line=dict(color="#00C851", width=3),
            fill="tozeroy",
            fillcolor="rgba(0,200,100,0.08)",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,10,20,0.9)",
            height=400, margin=dict(t=20, b=40, l=60, r=20),
            xaxis=dict(title=LABELS[param], gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", tickfont={"color":"#7A9BB5"}),
            yaxis=dict(title="Rendement prevu (t/ha)", gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", tickfont={"color":"#7A9BB5"}),
            font_color="#C8D8E8",
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Min / Max
        y_arr = np.array(ys)
        x_max = xs[np.argmax(y_arr)]
        st.markdown(f"""
        <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:0.5rem;">
            <div class="glass-card" style="flex:1;min-width:120px;text-align:center;padding:1rem;">
                <div style="font-size:0.72rem;color:#7A9BB5;text-transform:uppercase;letter-spacing:0.08em;">Rendement max</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:#00C851;">{y_arr.max():.2f} t/ha</div>
            </div>
            <div class="glass-card" style="flex:1;min-width:120px;text-align:center;padding:1rem;">
                <div style="font-size:0.72rem;color:#7A9BB5;text-transform:uppercase;letter-spacing:0.08em;">Valeur optimale</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:#0096FF;">{x_max:.1f}</div>
            </div>
            <div class="glass-card" style="flex:1;min-width:120px;text-align:center;padding:1rem;">
                <div style="font-size:0.72rem;color:#7A9BB5;text-transform:uppercase;letter-spacing:0.08em;">Rendement min</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:#FF7A50;">{y_arr.min():.2f} t/ha</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
