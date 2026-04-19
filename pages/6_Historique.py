import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_theme, page_header
from models.predict import predict_yield

st.set_page_config(page_title="Historique · AgroPredict SN", layout="wide")
inject_theme(active_page="Historique")

page_header("Historique & Comparaison", "Tendances des rendements 2000-2023 et comparaison saison N vs N-1")

# Initialisation de la liste des predictions en session (persistante pendant la navigation)
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

try:
    df_raw = pd.read_csv("data/raw/senegal_yield_data.csv")
except Exception:
    st.error("Dataset introuvable.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["📈  Tendances historiques", "🔄  Saison N vs N-1", "📋  Mes prédictions"])

with tab1:
    st.markdown("<div class='section-title fade-in'>Evolution des rendements 2000-2023</div>", unsafe_allow_html=True)

    col_ctrl, col_chart = st.columns([1, 3])
    with col_ctrl:
        crops_sel   = st.multiselect("Cultures", df_raw["crop"].unique().tolist(), default=["Arachide", "Riz"])
        regions_sel = st.multiselect("Regions", df_raw["region"].unique().tolist(), default=df_raw["region"].unique().tolist())
        smooth      = st.checkbox("Lissage (moyenne mobile 3 ans)", value=True)

    with col_chart:
        # Filtrage et calcul de la moyenne annuelle par culture
        df_f     = df_raw[df_raw["crop"].isin(crops_sel) & df_raw["region"].isin(regions_sel)]
        df_trend = df_f.groupby(["year", "crop"])["yield_ton_ha"].mean().reset_index()

        if smooth:
            # Moyenne mobile sur 3 ans pour lisser les variations annuelles
            df_trend["yield_ton_ha"] = df_trend.groupby("crop")["yield_ton_ha"].transform(
                lambda x: x.rolling(3, min_periods=1, center=True).mean()
            )

        COLORS = {"Arachide": "#00C851", "Mil": "#0096FF", "Mais": "#FFD060", "Riz": "#D080FF", "Sorgho": "#FF7A50"}
        fig = go.Figure()
        for crop in crops_sel:
            d = df_trend[df_trend["crop"] == crop]
            fig.add_trace(go.Scatter(
                x=d["year"], y=d["yield_ton_ha"],
                mode="lines+markers",
                name=crop,
                line=dict(color=COLORS.get(crop, "#FFF"), width=2.5),
                marker=dict(size=6),
                fill="tozeroy" if len(crops_sel) == 1 else None,
                fillcolor=f"rgba(0,200,100,0.05)" if len(crops_sel) == 1 else None,
            ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,10,20,0.9)",
            height=380, margin=dict(t=10, b=40, l=60, r=20),
            legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#C8D8E8"),
            xaxis=dict(title="Annee", gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", tickfont={"color":"#7A9BB5"}),
            yaxis=dict(title="Rendement moyen (t/ha)", gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", tickfont={"color":"#7A9BB5"}),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap : tableau croise region x culture
    st.markdown("<div class='section-title fade-in' style='font-size:1.1rem;margin-top:1rem;'>Rendement moyen par region et culture</div>", unsafe_allow_html=True)
    pivot = df_raw.groupby(["region", "crop"])["yield_ton_ha"].mean().reset_index().pivot(index="region", columns="crop", values="yield_ton_ha").round(2)
    fig_hm = px.imshow(
        pivot, text_auto=True, color_continuous_scale="Greens",
        labels={"color": "t/ha"},
    )
    fig_hm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=280, margin=dict(t=10, b=10, l=10, r=10),
        font_color="#C8D8E8", coloraxis_colorbar=dict(tickfont={"color": "#7A9BB5"}),
    )
    st.plotly_chart(fig_hm, use_container_width=True)

with tab2:
    st.markdown("<div class='section-title fade-in'>Comparaison saison N vs N-1</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        year_n  = st.selectbox("Annee N (recente)", sorted(df_raw["year"].unique(), reverse=True), index=0)
    with col_b:
        year_n1 = st.selectbox("Annee N-1 (reference)", sorted(df_raw["year"].unique(), reverse=True), index=1)

    crop_cmp = st.selectbox("Culture", df_raw["crop"].unique().tolist(), key="cmp_crop")

    # Calcul des rendements moyens par region pour les deux annees
    d_n  = df_raw[(df_raw["year"] == year_n)  & (df_raw["crop"] == crop_cmp)].groupby("region")["yield_ton_ha"].mean()
    d_n1 = df_raw[(df_raw["year"] == year_n1) & (df_raw["crop"] == crop_cmp)].groupby("region")["yield_ton_ha"].mean()
    df_cmp = pd.DataFrame({"N": d_n, "N-1": d_n1}).dropna().reset_index()
    df_cmp["delta"]     = (df_cmp["N"] - df_cmp["N-1"]).round(3)
    df_cmp["delta_pct"] = ((df_cmp["delta"] / df_cmp["N-1"]) * 100).round(1)

    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(name=f"N-1 ({year_n1})", x=df_cmp["region"], y=df_cmp["N-1"],
                             marker_color="rgba(0,150,255,0.5)", marker_line_color="#0096FF", marker_line_width=1))
    fig_cmp.add_trace(go.Bar(name=f"N ({year_n})", x=df_cmp["region"], y=df_cmp["N"],
                             marker_color="rgba(0,200,100,0.6)", marker_line_color="#00C851", marker_line_width=1))
    fig_cmp.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,10,20,0.9)",
        height=340, margin=dict(t=10, b=40, l=60, r=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#C8D8E8"),
        xaxis=dict(gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", tickfont={"color":"#C8D8E8"}),
        yaxis=dict(title="Rendement (t/ha)", gridcolor="rgba(0,200,100,0.06)", color="#7A9BB5", tickfont={"color":"#7A9BB5"}),
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Delta cards
    cols = st.columns(min(len(df_cmp), 7))
    for col, (_, row_d) in zip(cols, df_cmp.iterrows()):
        color = "#00C851" if row_d["delta"] >= 0 else "#FF3C3C"
        sign  = "+" if row_d["delta"] >= 0 else ""
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:0.8rem 0.5rem;border-color:{color}30;">
                <div style="font-size:0.68rem;color:#7A9BB5;">{row_d['region']}</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;color:{color};">{sign}{row_d['delta_pct']}%</div>
                <div style="font-size:0.7rem;color:#3A5A7A;">{sign}{row_d['delta']:.2f} t/ha</div>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='section-title fade-in'>Historique de mes predictions</div>", unsafe_allow_html=True)

    # Formulaire pour ajouter manuellement une prediction a l'historique
    with st.expander("Ajouter une prediction", expanded=not st.session_state.prediction_history):
        c1, c2, c3 = st.columns(3)
        with c1:
            h_region = st.selectbox("Region", df_raw["region"].unique().tolist(), key="h_reg")
            h_crop   = st.selectbox("Culture", df_raw["crop"].unique().tolist(), key="h_crop")
        with c2:
            h_rain = st.slider("Pluie (mm)", 200, 1200, 650, key="h_rain")
            h_temp = st.slider("Temperature (C)", 24.0, 33.0, 27.5, step=0.1, key="h_temp")
        with c3:
            h_ndvi = st.slider("NDVI", 0.30, 0.92, 0.65, step=0.01, key="h_ndvi")
            h_note = st.text_input("Note (optionnel)", placeholder="Ex: parcelle pilote Thies nord")

        if st.button("Enregistrer la prediction", type="primary"):
            pred = predict_yield(h_region, h_crop, h_rain, h_temp, h_ndvi)
            st.session_state.prediction_history.append({
                "region": h_region, "culture": h_crop,
                "pluie_mm": h_rain, "temp_c": h_temp, "ndvi": h_ndvi,
                "rendement_t_ha": pred, "note": h_note,
            })
            st.success(f"Prediction enregistree : {pred:.2f} t/ha")

    if st.session_state.prediction_history:
        df_hist = pd.DataFrame(st.session_state.prediction_history)
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

        # Export CSV
        csv = df_hist.to_csv(index=False).encode("utf-8")
        st.download_button("Telecharger CSV", csv, "predictions_agropreddict.csv", "text/csv")

        if st.button("Vider l'historique"):
            st.session_state.prediction_history = []
            st.rerun()
    else:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2rem;color:#3A5A7A;">
            Aucune prediction enregistree. Utilisez le formulaire ci-dessus.
        </div>
        """, unsafe_allow_html=True)
