import streamlit as st

CORPORATE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ===== BASE ===== */
html, body, [data-testid="stApp"] {
    background: #050A0F !important;
    color: #E8EDF2 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070D14 0%, #0A1520 100%) !important;
    border-right: 1px solid rgba(0,200,100,0.15) !important;
}
[data-testid="stSidebar"] * { color: #C8D8E8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { color: #7A9BB5 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background: rgba(0,200,100,0.06) !important; border: 1px solid rgba(0,200,100,0.2) !important; border-radius: 8px !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div { background: rgba(0,200,100,0.3) !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] [aria-valuenow] { background: #00C851 !important; border: 2px solid #00FF77 !important; }

/* ===== MAIN CONTENT ===== */
.main .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px !important; }

/* ===== HIDE DEFAULT ELEMENTS ===== */
#MainMenu, footer { visibility: hidden !important; }
header { visibility: hidden !important; height: 0 !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ===== TOPBAR FIXE ===== */
#agro-topbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
    height: 52px;
    background: rgba(5,10,15,0.92);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(0,200,100,0.18);
    display: flex; align-items: center;
    padding: 0 1.5rem; gap: 0;
}
#agro-topbar .tb-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: #E8EDF2; white-space: nowrap;
    margin-right: 2rem;
}
#agro-topbar .tb-logo span { color: #00C851; }
#agro-topbar nav { display: flex; gap: 0.25rem; flex: 1; }
#agro-topbar nav a {
    color: #7A9BB5; font-size: 0.82rem; font-weight: 500;
    text-decoration: none; padding: 0.35rem 0.85rem;
    border-radius: 8px; transition: all 0.18s;
    white-space: nowrap;
}
#agro-topbar nav a:hover { color: #E8EDF2; background: rgba(0,200,100,0.10); }
#agro-topbar nav a.active { color: #00C851; background: rgba(0,200,100,0.12); }
#agro-topbar .tb-badge {
    font-size: 0.72rem; font-weight: 600;
    background: rgba(0,200,100,0.12);
    border: 1px solid rgba(0,200,100,0.3);
    border-radius: 20px; padding: 0.2rem 0.7rem;
    color: #00C851; white-space: nowrap; margin-left: 1rem;
}

/* Compense la topbar fixe */
.main .block-container { padding-top: 4.5rem !important; }
[data-testid="stSidebar"] { padding-top: 52px !important; top: 52px !important; }

/* Collapse button reste visible */
[data-testid="collapsedControl"] {
    top: 60px !important;
    background: rgba(5,10,15,0.9) !important;
    border: 1px solid rgba(0,200,100,0.2) !important;
    border-radius: 0 8px 8px 0 !important;
}
[data-testid="collapsedControl"] svg { color: #00C851 !important; }

/* ===== TABS ===== */
[data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid rgba(0,200,100,0.2) !important; gap: 0.5rem; }
[data-baseweb="tab"] { background: transparent !important; color: #7A9BB5 !important; border-radius: 8px 8px 0 0 !important; padding: 0.6rem 1.2rem !important; font-weight: 500 !important; font-size: 0.9rem !important; transition: all 0.2s !important; border: none !important; }
[aria-selected="true"][data-baseweb="tab"] { background: rgba(0,200,100,0.1) !important; color: #00C851 !important; border-bottom: 2px solid #00C851 !important; }
[data-baseweb="tab"]:hover { color: #00C851 !important; background: rgba(0,200,100,0.05) !important; }

/* ===== SELECTBOX & INPUTS ===== */
[data-baseweb="select"] > div { background: rgba(10,30,50,0.8) !important; border: 1px solid rgba(0,200,100,0.25) !important; border-radius: 10px !important; color: #E8EDF2 !important; }
[data-baseweb="select"] > div:focus-within { border-color: #00C851 !important; box-shadow: 0 0 0 3px rgba(0,200,100,0.15) !important; }
[data-baseweb="menu"] { background: #0A1520 !important; border: 1px solid rgba(0,200,100,0.2) !important; }
[data-baseweb="option"] { background: transparent !important; color: #C8D8E8 !important; }
[data-baseweb="option"]:hover { background: rgba(0,200,100,0.1) !important; }

/* ===== SLIDERS ===== */
[data-testid="stSlider"] [role="slider"] { background: #00C851 !important; border: 2px solid #00FF77 !important; width: 18px !important; height: 18px !important; box-shadow: 0 0 12px rgba(0,200,100,0.5) !important; }
[data-testid="stSlider"] [data-testid="stSlider"] > div > div:first-child { background: rgba(0,200,100,0.25) !important; }

/* ===== BUTTONS ===== */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #00C851, #00A844) !important;
    border: none !important; border-radius: 10px !important;
    color: #fff !important; font-weight: 600 !important;
    font-size: 0.95rem !important; padding: 0.7rem 1.5rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(0,200,100,0.35) !important;
}
[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,200,100,0.5) !important;
    background: linear-gradient(135deg, #00FF77, #00C851) !important;
}
[data-testid="baseButton-secondary"] {
    background: transparent !important;
    border: 1px solid rgba(0,200,100,0.4) !important;
    border-radius: 10px !important; color: #00C851 !important;
}

/* ===== METRICS ===== */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,200,100,0.06), rgba(0,100,200,0.04)) !important;
    border: 1px solid rgba(0,200,100,0.2) !important;
    border-radius: 14px !important; padding: 1.2rem 1.5rem !important;
    backdrop-filter: blur(10px) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px) !important; box-shadow: 0 8px 30px rgba(0,200,100,0.15) !important; }
[data-testid="stMetricLabel"] { color: #7A9BB5 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: #00C851 !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 2rem !important; font-weight: 700 !important; }

/* ===== ALERTS ===== */
[data-testid="stAlert"] { border-radius: 12px !important; border-left-width: 4px !important; backdrop-filter: blur(8px) !important; }
.stSuccess { background: rgba(0,200,100,0.08) !important; border-color: #00C851 !important; color: #7EFFC0 !important; }
.stWarning { background: rgba(255,160,0,0.08) !important; border-color: #FFA000 !important; color: #FFD580 !important; }
.stError   { background: rgba(255,60,60,0.08) !important; border-color: #FF3C3C !important; color: #FF9A9A !important; }
.stInfo    { background: rgba(0,150,255,0.08) !important; border-color: #0096FF !important; color: #80CFFF !important; }

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; border: 1px solid rgba(0,200,100,0.15) !important; }

/* ===== DIVIDER ===== */
hr { border-color: rgba(0,200,100,0.15) !important; }

/* ===== SPINNER ===== */
[data-testid="stSpinner"] > div { border-top-color: #00C851 !important; }

/* ===== ANIMATIONS ===== */
@keyframes fadeInUp { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }
@keyframes pulse-glow { 0%,100% { box-shadow:0 0 20px rgba(0,200,100,0.3); } 50% { box-shadow:0 0 40px rgba(0,200,100,0.6); } }
@keyframes shimmer { 0% { background-position: -200% center; } 100% { background-position: 200% center; } }
@keyframes float { 0%,100% { transform:translateY(0px); } 50% { transform:translateY(-8px); } }

.fade-in { animation: fadeInUp 0.6s ease both; }
.fade-in-2 { animation: fadeInUp 0.6s ease 0.15s both; }
.fade-in-3 { animation: fadeInUp 0.6s ease 0.3s both; }

/* ===== GLASS CARD ===== */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,200,100,0.15);
    border-radius: 16px; padding: 1.5rem;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}
.glass-card:hover { border-color: rgba(0,200,100,0.35); background: rgba(0,200,100,0.04); transform: translateY(-2px); }

/* ===== STAT BADGE ===== */
.stat-badge {
    display:inline-block; background: rgba(0,200,100,0.12);
    border: 1px solid rgba(0,200,100,0.3); border-radius: 20px;
    padding: 0.3rem 0.9rem; font-size:0.8rem; font-weight:600;
    color: #00C851; letter-spacing:0.05em;
}

/* ===== SECTION TITLE ===== */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem; font-weight: 700;
    background: linear-gradient(135deg, #E8EDF2, #00C851);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.section-sub { color: #7A9BB5; font-size: 0.9rem; margin-bottom: 1.5rem; }

/* ===== PAGE HEADER ===== */
.page-header {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid rgba(0,200,100,0.12);
    margin-bottom: 2rem;
}
</style>
"""

HERO_3D = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&family=Inter:wght@400;500&display=swap');
#hero-root { position:relative; width:100%; height:360px; border-radius:20px; overflow:hidden;
  margin-bottom:2rem; border:1px solid rgba(0,200,100,0.2); background:#050A0F; }
#globe-canvas { position:absolute; right:0; top:0; height:100%; width:50%; opacity:0.9; }
#hero-text { position:absolute; left:0; top:0; height:100%; width:55%; display:flex;
  flex-direction:column; justify-content:center; padding:2.5rem; z-index:3; }
.hero-eyebrow { font-family:'Space Grotesk',sans-serif; font-size:0.72rem; font-weight:700;
  color:#00C851; text-transform:uppercase; letter-spacing:0.18em; margin-bottom:0.8rem;
  animation: fadeUp 0.6s ease both; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:2.8rem; font-weight:800;
  color:#E8EDF2; line-height:1.05; margin:0 0 0.9rem;
  animation: fadeUp 0.6s ease 0.1s both; }
.hero-sub { font-family:'Inter',sans-serif; color:#7A9BB5; font-size:0.9rem; max-width:420px;
  line-height:1.7; margin:0 0 1.5rem; animation: fadeUp 0.6s ease 0.2s both; }
.hero-badges { display:flex; gap:0.7rem; flex-wrap:wrap; animation: fadeUp 0.6s ease 0.3s both; }
.hbadge { border-radius:20px; padding:0.3rem 0.9rem; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; }
@keyframes fadeUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:none} }
</style>

<div id="hero-root">
  <canvas id="globe-canvas"></canvas>
  <div id="hero-text">
    <div class="hero-eyebrow">Plateforme Agricole &middot; Sénégal</div>
    <div class="hero-title">AgroPredict <span style="color:#00C851;">SN</span></div>
    <div class="hero-sub">Prédiction des rendements par XGBoost &middot; 6 163 observations &middot; 26 variables &middot; Sources : FAOSTAT, NASA POWER, DAPSA</div>
    <div class="hero-badges">
      <span class="hbadge" style="background:rgba(0,200,100,0.12);border:1px solid rgba(0,200,100,0.35);color:#00C851;">R² = 0.989</span>
      <span class="hbadge" style="background:rgba(0,150,255,0.1);border:1px solid rgba(0,150,255,0.3);color:#60BFFF;">6 163 obs.</span>
      <span class="hbadge" style="background:rgba(255,200,0,0.08);border:1px solid rgba(255,200,0,0.25);color:#FFD060;">26 variables</span>
      <span class="hbadge" style="background:rgba(200,0,255,0.08);border:1px solid rgba(200,0,255,0.2);color:#D080FF;">7 régions</span>
      <span class="hbadge" style="background:rgba(255,120,0,0.08);border:1px solid rgba(255,120,0,0.2);color:#FF9A50;">2000-2023</span>
    </div>
  </div>
</div>

<script>
(function(){
  const canvas = document.getElementById('globe-canvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize(){
    canvas.width  = canvas.offsetWidth  * window.devicePixelRatio;
    canvas.height = canvas.offsetHeight * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }
  resize();

  const W = () => canvas.offsetWidth;
  const H = () => canvas.offsetHeight;
  const PI = Math.PI;
  let t = 0;

  // Globe parameters
  const R = () => Math.min(W(), H()) * 0.40;
  const cx = () => W() * 0.52;
  const cy = () => H() * 0.50;

  // Senegal region dots (lat/lon -> 3D sphere)
  const POINTS = [
    {lat:14.79,lon:-16.93,label:"Thiès",    color:"#00C851", r:5},
    {lat:14.34,lon:-16.41,label:"Fatick",   color:"#0096FF", r:4.5},
    {lat:14.15,lon:-16.07,label:"Kaolack",  color:"#FFD060", r:5},
    {lat:16.02,lon:-16.49,label:"St-Louis", color:"#D080FF", r:5},
    {lat:14.10,lon:-15.55,label:"Kaffrine", color:"#FF7A50", r:4},
    {lat:13.77,lon:-13.67,label:"Tamba",    color:"#00D4FF", r:4},
    {lat:12.71,lon:-15.56,label:"Sedhiou",  color:"#FF50A0", r:4},
  ];

  // Africa outline (simplified SVG path points, lat/lon)
  function latLonTo3D(lat, lon, radius, rotY) {
    const phi   = (90 - lat) * PI / 180;
    const theta = (lon + 180) * PI / 180 + rotY;
    return {
      x: radius * Math.sin(phi) * Math.cos(theta),
      y: radius * Math.cos(phi),
      z: radius * Math.sin(phi) * Math.sin(theta),
    };
  }

  function project(p3, cx, cy) {
    const fov = 600;
    const z = p3.z + 600;
    return { x: cx + p3.x * fov / z, y: cy - p3.y * fov / z, scale: fov / z };
  }

  // Generate lat/lon grid lines
  const gridLines = [];
  for(let lat=-80;lat<=80;lat+=20){
    const line=[];
    for(let lon=-180;lon<=180;lon+=5) line.push({lat,lon});
    gridLines.push(line);
  }
  for(let lon=-180;lon<=180;lon+=30){
    const line=[];
    for(let lat=-85;lat<=85;lat+=5) line.push({lat,lon});
    gridLines.push(line);
  }

  function draw(){
    ctx.clearRect(0,0,W(),H());
    const r   = R();
    const rotY= t * 0.008;
    const cx_ = cx(), cy_ = cy();

    // Glow behind globe
    const grd = ctx.createRadialGradient(cx_,cy_,r*0.2,cx_,cy_,r*1.4);
    grd.addColorStop(0,'rgba(0,200,100,0.06)');
    grd.addColorStop(0.5,'rgba(0,100,200,0.04)');
    grd.addColorStop(1,'transparent');
    ctx.fillStyle=grd; ctx.beginPath();
    ctx.arc(cx_,cy_,r*1.4,0,PI*2); ctx.fill();

    // Globe base
    const globeGrd = ctx.createRadialGradient(cx_-r*0.25,cy_-r*0.2,r*0.05,cx_,cy_,r);
    globeGrd.addColorStop(0,'rgba(0,40,20,0.55)');
    globeGrd.addColorStop(0.6,'rgba(0,20,35,0.45)');
    globeGrd.addColorStop(1,'rgba(0,5,15,0.30)');
    ctx.beginPath(); ctx.arc(cx_,cy_,r,0,PI*2);
    ctx.fillStyle=globeGrd; ctx.fill();
    ctx.strokeStyle='rgba(0,200,100,0.20)'; ctx.lineWidth=1.5; ctx.stroke();

    // Grid lines
    ctx.lineWidth=0.6;
    gridLines.forEach(line=>{
      let started=false;
      ctx.beginPath();
      line.forEach(({lat,lon})=>{
        const p3=latLonTo3D(lat,lon,r,rotY);
        const visible=p3.z>-r*0.15;
        const pp=project(p3,cx_,cy_);
        if(!started){ ctx.moveTo(pp.x,pp.y); started=true; }
        else { visible ? ctx.lineTo(pp.x,pp.y) : ctx.moveTo(pp.x,pp.y); }
      });
      ctx.strokeStyle='rgba(0,200,100,0.07)'; ctx.stroke();
    });

    // Region dots
    POINTS.forEach(pt=>{
      const p3=latLonTo3D(pt.lat,pt.lon,r,rotY);
      if(p3.z<-r*0.1) return; // hidden side
      const pp=project(p3,cx_,cy_);
      const rs=pt.r*pp.scale*18;

      // Pulse ring
      const pulse=(Math.sin(t*0.05+pt.lon)*0.5+0.5);
      ctx.beginPath(); ctx.arc(pp.x,pp.y,rs*(1+pulse*0.8),0,PI*2);
      ctx.strokeStyle=pt.color+'50'; ctx.lineWidth=1; ctx.stroke();

      // Dot
      const dg=ctx.createRadialGradient(pp.x,pp.y,0,pp.x,pp.y,rs);
      dg.addColorStop(0,pt.color+'FF');
      dg.addColorStop(0.5,pt.color+'AA');
      dg.addColorStop(1,pt.color+'00');
      ctx.beginPath(); ctx.arc(pp.x,pp.y,rs,0,PI*2);
      ctx.fillStyle=dg; ctx.fill();

      // Label
      if(pp.scale>0.8){
        ctx.font=`bold ${Math.round(8*pp.scale)}px Inter,sans-serif`;
        ctx.fillStyle='rgba(220,240,255,0.85)';
        ctx.fillText(pt.label, pp.x+rs+2, pp.y+3);
      }
    });

    // Atmosphere rim
    const rim=ctx.createRadialGradient(cx_,cy_,r*0.92,cx_,cy_,r*1.08);
    rim.addColorStop(0,'rgba(0,200,100,0.00)');
    rim.addColorStop(0.5,'rgba(0,200,100,0.06)');
    rim.addColorStop(1,'rgba(0,200,100,0.00)');
    ctx.beginPath(); ctx.arc(cx_,cy_,r*1.08,0,PI*2);
    ctx.fillStyle=rim; ctx.fill();

    // Highlight
    const hl=ctx.createRadialGradient(cx_-r*0.30,cy_-r*0.28,0,cx_-r*0.10,cy_-r*0.10,r*0.7);
    hl.addColorStop(0,'rgba(255,255,255,0.06)');
    hl.addColorStop(1,'transparent');
    ctx.beginPath(); ctx.arc(cx_,cy_,r,0,PI*2);
    ctx.fillStyle=hl; ctx.fill();

    t++;
    requestAnimationFrame(draw);
  }
  draw();
  window.addEventListener('resize', ()=>{ resize(); });
})();
</script>
"""


TOPBAR_HTML = """
<div id="agro-topbar">
  <div class="tb-logo">🌾 AgroPredict <span>SN</span></div>
  <nav>
    <a href="/" target="_self">Accueil</a>
    <a href="/Prediction_Rendements" target="_self">Prédiction</a>
    <a href="/Carte_Interactive" target="_self">Carte</a>
    <a href="/Recommandations" target="_self">Recommandations</a>
    <a href="/Analyse_SHAP" target="_self">Analyse</a>
    <a href="/Historique" target="_self">Historique</a>
    <a href="/About" target="_self">À propos</a>
  </nav>
  <span class="tb-badge">R² 0.990</span>
</div>
"""


def inject_theme(active_page=""):
    st.markdown(CORPORATE_CSS, unsafe_allow_html=True)
    # Marque la page active dans la nav
    topbar = TOPBAR_HTML
    if active_page:
        topbar = topbar.replace(
            f'href="/{active_page}" target="_self">',
            f'href="/{active_page}" target="_self" class="active">',
        )
    st.markdown(topbar, unsafe_allow_html=True)


def render_hero():
    st.iframe(HERO_3D, height=340) if hasattr(st, "iframe") else st.components.v1.html(HERO_3D, height=340)


def page_header(title, subtitle=""):
    st.markdown(f"""
    <div class="page-header fade-in">
        <div class="section-title">{title}</div>
        {"<div class='section-sub'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def glass_card(content_html):
    st.markdown(f'<div class="glass-card fade-in">{content_html}</div>', unsafe_allow_html=True)


def kpi_row(items):
    """items = list of (label, value, color_hex)"""
    cols = st.columns(len(items))
    for col, (label, value, color) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="glass-card fade-in" style="text-align:center;border-color:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.3);">
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:#7A9BB5;margin-bottom:0.4rem;">{label}</div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:1.9rem;font-weight:700;color:{color};">{value}</div>
            </div>
            """, unsafe_allow_html=True)
