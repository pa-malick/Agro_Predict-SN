import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from models.predict import predict_yield
from utils.theme import inject_theme, page_header

st.set_page_config(page_title="Carte · AgroPredict SN", layout="wide")
inject_theme(active_page="Carte_Interactive")

page_header("Carte interactive · Sénégal", "Rendements prévus par région selon les conditions climatiques")

REGIONS_COORDS = {
    "Thiès":        [14.79, -16.93],
    "Fatick":       [14.34, -16.41],
    "Kaolack":      [14.15, -16.07],
    "Saint-Louis":  [16.02, -16.49],
    "Kaffrine":     [14.10, -15.55],
    "Tambacounda":  [13.77, -13.67],
    "Sédhiou":      [12.71, -15.56],
}

col_ctrl, col_map = st.columns([1, 3], gap="large")

with col_ctrl:
    st.markdown("""
    <div class="glass-card fade-in" style="padding:1.5rem;">
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:1rem;">Simulation</div>
    """, unsafe_allow_html=True)

    crop     = st.selectbox("Culture", ["Arachide", "Mil", "Maïs", "Riz", "Sorgho"])
    rainfall = st.slider("Pluie (mm)", 200, 1200, 650)
    temp     = st.slider("Température (°C)", 24.0, 33.0, 27.5, step=0.1)
    ndvi     = st.slider("NDVI", 0.30, 0.92, 0.65, step=0.01)

    st.markdown("</div>", unsafe_allow_html=True)

    preds = {r: predict_yield(r, crop, rainfall, temp, ndvi) for r in REGIONS_COORDS}

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:0.7rem;">Classement</div>
    """, unsafe_allow_html=True)

    sorted_preds = sorted(preds.items(), key=lambda x: x[1], reverse=True)
    for i, (reg, val) in enumerate(sorted_preds):
        medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
        bar_w = int((val / max(preds.values())) * 100)
        st.markdown(f"""
        <div style="margin-bottom:0.6rem;">
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;margin-bottom:0.2rem;">
                <span style="color:#C8D8E8;">{medal} {reg}</span>
                <span style="color:#00C851;font-weight:600;">{val:.2f} t/ha</span>
            </div>
            <div style="height:4px;background:rgba(255,255,255,0.05);border-radius:4px;">
                <div style="height:4px;width:{bar_w}%;background:linear-gradient(90deg,#00C851,#0096FF);border-radius:4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_map:
    m = folium.Map(
        location=[14.5, -14.8],
        zoom_start=7,
        tiles="CartoDB dark_matter",
    )

    max_pred = max(preds.values())
    min_pred = min(preds.values())

    for reg, coords in REGIONS_COORDS.items():
        val = preds.get(reg, 1.5)
        ratio = (val - min_pred) / (max_pred - min_pred + 0.001)
        r_c = int(255 * (1 - ratio))
        g_c = int(200 * ratio + 55)
        color_hex = f"#{r_c:02x}{g_c:02x}55"

        popup_html = f"""
        <div style="font-family:Inter,sans-serif;min-width:160px;background:#0A1520;color:#E8EDF2;border-radius:8px;padding:12px;border:1px solid rgba(0,200,100,0.3);">
            <div style="font-weight:700;font-size:1rem;color:#00C851;margin-bottom:6px;">{reg}</div>
            <div style="font-size:0.85rem;color:#7A9BB5;">Culture : <b style="color:#E8EDF2;">{crop}</b></div>
            <div style="font-size:1.4rem;font-weight:800;color:#00C851;margin-top:6px;">{val:.2f} t/ha</div>
            <div style="font-size:0.75rem;color:#3A5A7A;margin-top:4px;">🌧 {rainfall}mm · 🌡 {temp}°C · 🌿 {ndvi}</div>
        </div>
        """

        folium.CircleMarker(
            location=coords,
            radius=14 + ratio * 12,
            color="#00C851",
            fill=True,
            fill_color=f"#{int(255*(1-ratio)):02x}{int(200*ratio+55):02x}55",
            fill_opacity=0.75,
            weight=2,
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{reg} · {val:.2f} t/ha",
        ).add_to(m)

        folium.Marker(
            location=coords,
            icon=folium.DivIcon(
                html=f'<div style="font-family:Space Grotesk,sans-serif;font-size:11px;font-weight:700;color:#fff;text-shadow:0 1px 4px #000;white-space:nowrap;transform:translateY(-28px);">{val:.2f}</div>',
                icon_size=(60, 20),
                icon_anchor=(30, 0),
            ),
        ).add_to(m)

    st_folium(m, width=None, height=540, use_container_width=True)
