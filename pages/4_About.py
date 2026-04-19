import streamlit as st
from utils.theme import inject_theme, page_header

st.set_page_config(page_title="À propos · AgroPredict SN", layout="wide")
inject_theme(active_page="About")

page_header("À propos", "Modélisation agricole au service du Sénégal")

st.markdown("""
<div style="max-width:900px;">

<div class="glass-card fade-in" style="margin-bottom:1.2rem;border-color:rgba(0,200,100,0.3);">
    <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#00C851;margin-bottom:1rem;">Mission</div>
    <p style="color:#C8D8E8;font-size:1rem;line-height:1.8;margin:0;">
    AgroPredict SN combine <b style="color:#E8EDF2;">données satellitaires</b> et <b style="color:#E8EDF2;">apprentissage automatique</b>
    pour aider les producteurs sénégalais, conseillers agricoles et décideurs à <b style="color:#00C851;">anticiper les rendements</b>
    avant la saison des pluies, réduisant ainsi les risques liés au changement climatique.
    </p>
</div>

</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="glass-card fade-in" style="height:100%;">
        <div style="font-size:1.8rem;margin-bottom:0.8rem;">📈</div>
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#00C851;margin-bottom:0.6rem;">Modèle ML</div>
        <ul style="color:#C8D8E8;font-size:0.88rem;line-height:2;padding-left:1.2rem;margin:0;">
            <li>XGBoost Gradient Boosting</li>
            <li>R² = 0.98 · RMSE = 0.13 t/ha</li>
            <li>535 observations · 7 régions</li>
            <li>Intervalle de confiance 95%</li>
            <li>Réentraînable automatiquement</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card fade-in-2" style="height:100%;">
        <div style="font-size:1.8rem;margin-bottom:0.8rem;">🛰️</div>
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#0096FF;margin-bottom:0.6rem;">Sources de données</div>
        <ul style="color:#C8D8E8;font-size:0.88rem;line-height:2;padding-left:1.2rem;margin:0;">
            <li>FAOSTAT · FAO</li>
            <li>NASA POWER API</li>
            <li>DAPSA / ANSD Sénégal</li>
            <li>CHIRPS (pluviométrie)</li>
            <li>Copernicus / MODIS (NDVI)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card fade-in-3" style="height:100%;">
        <div style="font-size:1.8rem;margin-bottom:0.8rem;">⚙️</div>
        <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#D080FF;margin-bottom:0.6rem;">DevOps & Stack</div>
        <ul style="color:#C8D8E8;font-size:0.88rem;line-height:2;padding-left:1.2rem;margin:0;">
            <li>CI/CD · GitHub Actions</li>
            <li>Docker · docker-compose</li>
            <li>Streamlit Cloud</li>
            <li>pytest · 17 tests</li>
            <li>Python 3.11 · XGBoost 2</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card fade-in" style="max-width:900px;display:flex;align-items:center;gap:2rem;flex-wrap:wrap;">
    <div style="width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#00C851,#0096FF);display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:800;color:#fff;font-family:'Space Grotesk',sans-serif;flex-shrink:0;">PM</div>
    <div style="flex:1;min-width:200px;">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.2rem;font-weight:700;color:#E8EDF2;">Papa Malick NDIAYE</div>
        <div style="color:#7A9BB5;font-size:0.9rem;margin-top:0.2rem;">Master 2 · Data Science & Génie Logiciel</div>
        <div style="margin-top:0.6rem;display:flex;gap:0.8rem;flex-wrap:wrap;">
            <span style="background:rgba(0,200,100,0.1);border:1px solid rgba(0,200,100,0.25);border-radius:20px;padding:0.25rem 0.8rem;font-size:0.78rem;color:#00C851;">njaymika@gmail.com</span>
            <span style="background:rgba(0,150,255,0.1);border:1px solid rgba(0,150,255,0.25);border-radius:20px;padding:0.25rem 0.8rem;font-size:0.78rem;color:#60BFFF;">Machine Learning</span>
            <span style="background:rgba(200,0,255,0.08);border:1px solid rgba(200,0,255,0.2);border-radius:20px;padding:0.25rem 0.8rem;font-size:0.78rem;color:#D080FF;">Data Engineering</span>
            <span style="background:rgba(255,160,0,0.08);border:1px solid rgba(255,160,0,0.2);border-radius:20px;padding:0.25rem 0.8rem;font-size:0.78rem;color:#FFD060;">DevOps</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
