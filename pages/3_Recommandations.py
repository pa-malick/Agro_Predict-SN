import streamlit as st
from models.predict import predict_yield
from utils.theme import inject_theme, page_header

st.set_page_config(page_title="Recommandations · AgroPredict SN", layout="wide")
inject_theme(active_page="Recommandations")

page_header("Recommandations agronomiques", "Conseils personnalisés basés sur la prédiction XGBoost")

SEMIS = {
    "Arachide": "15 juin – 5 juillet",
    "Mil":      "20 juin – 10 juillet",
    "Maïs":     "1 – 20 juillet",
    "Riz":      "Juin (pluvial) · Toute l'année (irrigué)",
    "Sorgho":   "1 – 25 juillet",
}

VARIETES = {
    "Arachide": [("55-437", "Précoce · Zone centre-nord"), ("Fleur 11", "Demi-précoce · Haut rendement"), ("GH 119-20", "Tardive · Zones humides")],
    "Mil":      [("Souna III", "Précoce · 75 jours"), ("IBV 8004", "Amélioré · Tolérant chaleur"), ("IKMP5", "Haut rendement · Zone soudanienne")],
    "Maïs":     [("DK 8031", "Hybride · 2.5+ t/ha"), ("Bastan", "Local · Rustique"), ("SAMAZ", "Tolérant sécheresse")],
    "Riz":      [("Sahel 108", "Irrigué · Saint-Louis"), ("CK 4", "Pluvial · Centre"), ("Nerica 4", "Upland · Zones humides")],
    "Sorgho":   [("CE 145-66", "Local · Adapté"), ("S 35", "Amélioré · +20% rendement"), ("IRAT 204", "Tolérant stress hydrique")],
}

SEUIL_IRRIGATION = {"Arachide": 500, "Mil": 400, "Maïs": 600, "Riz": 800, "Sorgho": 400}

ICON = {"Arachide": "🥜", "Mil": "🌾", "Maïs": "🌽", "Riz": "🍚", "Sorgho": "🌿"}

col_form, col_reco = st.columns([1, 2], gap="large")

with col_form:
    st.markdown('<div class="glass-card fade-in" style="padding:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:1rem;">Votre situation</div>', unsafe_allow_html=True)

    region   = st.selectbox("Région", ["Thiès", "Fatick", "Kaolack", "Saint-Louis", "Kaffrine", "Tambacounda", "Sédhiou"])
    crop     = st.selectbox("Culture", list(SEMIS.keys()))
    rainfall = st.slider("Pluie attendue (mm)", 200, 1200, 650)
    temp     = st.slider("Température (°C)", 24.0, 33.0, 27.5, step=0.1)
    ndvi     = st.slider("NDVI végétation", 0.30, 0.92, 0.65, step=0.01)

    st.markdown("</div>", unsafe_allow_html=True)
    go_btn = st.button("Générer les recommandations", type="primary", use_container_width=True)

with col_reco:
    if go_btn:
        pred = predict_yield(region, crop, rainfall, temp, ndvi)
        seuil = SEUIL_IRRIGATION[crop]
        deficit = seuil - rainfall
        need_irrig = rainfall < seuil
        hot = temp > 30.5
        icon = ICON.get(crop, "🌱")

        # Score de risque
        risk = 0
        if pred < 0.8:
            risk = 3
        elif pred < 1.3:
            risk = 2
        elif pred < 2.0:
            risk = 1
        risk_label = ["Faible", "Modéré", "Élevé", "Critique"][risk]
        risk_color = ["#00C851", "#FFD060", "#FFA000", "#FF3C3C"][risk]

        st.markdown(f"""
        <div class="glass-card fade-in" style="border-color:rgba(0,200,100,0.4);margin-bottom:1.2rem;">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
                <div>
                    <div style="font-size:2.5rem;line-height:1;">{icon}</div>
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.8rem;font-weight:700;color:#00C851;">{pred:.2f} t/ha</div>
                    <div style="color:#7A9BB5;font-size:0.85rem;">{crop} · {region}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:0.4rem;">Niveau de risque</div>
                    <div style="background:{risk_color}18;border:1px solid {risk_color}40;border-radius:10px;padding:0.5rem 1.2rem;color:{risk_color};font-weight:700;font-size:1rem;">{risk_label}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Calendrier semis
        st.markdown(f"""
        <div class="glass-card fade-in" style="margin-bottom:1rem;">
            <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#0096FF;margin-bottom:0.7rem;">📅 Calendrier de semis</div>
            <div style="font-size:1rem;color:#E8EDF2;font-weight:500;">{SEMIS[crop]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Variétés
        st.markdown('<div class="glass-card fade-in" style="margin-bottom:1rem;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#D080FF;margin-bottom:0.7rem;">🌱 Variétés recommandées</div>', unsafe_allow_html=True)
        for name, desc in VARIETES[crop]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);">
                <div style="width:8px;height:8px;border-radius:50%;background:#D080FF;flex-shrink:0;"></div>
                <div>
                    <span style="color:#E8EDF2;font-weight:600;">{name}</span>
                    <span style="color:#7A9BB5;font-size:0.82rem;"> · {desc}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Irrigation
        irrig_color = "#FFA000" if need_irrig else "#00C851"
        irrig_msg = (
            f"Déficit hydrique : {deficit} mm sous le seuil de {seuil} mm. Irrigation complémentaire recommandée."
            if need_irrig else
            f"Pluviométrie suffisante ({rainfall} mm ≥ {seuil} mm). Irrigation non nécessaire."
        )
        irrig_icon = "⚠️" if need_irrig else "✅"
        st.markdown(f"""
        <div class="glass-card fade-in" style="border-color:{irrig_color}30;margin-bottom:1rem;">
            <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:{irrig_color};margin-bottom:0.5rem;">{irrig_icon} Gestion de l'eau</div>
            <div style="color:#C8D8E8;font-size:0.9rem;">{irrig_msg}</div>
        </div>
        """, unsafe_allow_html=True)

        if hot:
            st.markdown("""
            <div class="glass-card fade-in" style="border-color:#FFA00030;">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#FFA000;margin-bottom:0.5rem;">🌡 Alerte thermique</div>
                <div style="color:#C8D8E8;font-size:0.9rem;">Température élevée détectée. Privilégiez les variétés tolérantes à la chaleur et un semis précoce en début de saison.</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="height:400px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1rem;">
            <div style="font-size:3.5rem;opacity:0.25;">🌱</div>
            <div style="color:#3A5A7A;font-size:0.95rem;">Renseignez votre situation et générez vos recommandations</div>
        </div>
        """, unsafe_allow_html=True)
