# import streamlit as st
# import streamlit.components.v1 as components
# import pandas as pd
# import sys, os
# import requests

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# st.set_page_config(
#     page_title="Market AI Intelligence System",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# our_company = "ACME Corp"
# competitor  = "Globex Inc"

# # ─── Global CSS ─────────────────────────────────────────
# st.markdown("""
# <style>
# html,body{background:#0a0a0a;color:#f0f0f0}
# </style>
# """, unsafe_allow_html=True)

# # ─── NAVBAR ─────────────────────────────────────────
# st.markdown(
#     '<div style="padding:12px;background:#111;text-align:center;font-weight:bold;">Market AI Intelligence</div>',
#     unsafe_allow_html=True
# )

# # ─── HERO ─────────────────────────────────────────
# components.html("""
# <div style="text-align:center;padding:40px;">
# <h1>Market AI Intelligence System</h1>
# <p>AI-powered competitor intelligence</p>
# </div>
# """, height=200)

# # ─── QUERY ─────────────────────────────────────────
# st.markdown("## 🔍 Ask the Intelligence Engine")

# user_query = st.text_input(
#     "",
#     placeholder="What are competitor pricing trends?"
# )

# run_query = False
# if user_query:
#     run_query = st.button("⚡ Generate Strategic Insight")

# # ─── TABS ─────────────────────────────────────────
# tab1, tab2, tab3 = st.tabs(["📊 Micro-Insights", "🤖 RAG Strategist", "📁 Data Sources"])

# # ─── TAB 1 ─────────────────────────────────────────
# with tab1:
#     st.subheader("Micro Insights")
#     st.info("Micro-insights will be connected via backend API next.")

# # ─── TAB 2 (RAG) ─────────────────────────────────────────
# with tab2:
#     st.subheader("Strategic LLM Querying")

#     rag_query = user_query if user_query else st.text_input(
#         "Ask something:", "What are market trends?"
#     )

#     if run_query or st.button("⚡ Generate Insight"):
#         with st.spinner("Querying RAG system..."):

#             st.write("Retrieving insights from real market data...")

#             try:
#                 res = requests.post(
#                     "http://localhost:8000/rag",
#                     json={"query": rag_query}
#                 )

#                 if res.status_code == 200:
#                     response = res.json()["answer"]
#                 else:
#                     response = "Error from backend"

#             except Exception:
#                 response = "Backend not connected. Make sure FastAPI server is running."

#             st.divider()
#             st.subheader("📊 Strategic Insight")
#             st.markdown(response)

# # ─── TAB 3 ─────────────────────────────────────────
# with tab3:
#     st.subheader("System Metrics")
#     c1, c2, c3 = st.columns(3)
#     c1.metric("Websites Scraped", "14")
#     c2.metric("Reviews Processed", "2450")
#     c3.metric("Wayback Snapshots", "5")

# # ─── FOOTER ─────────────────────────────────────────
# st.markdown("---")
# st.markdown("Market AI Intelligence System © 2026")


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sys, os
import requests

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# try:
#     from nlp.insight_engine import generate_micro_insights, compute_aspect_sentiment
# except ImportError as e:
#     pass  # backend not loaded — UI still works

st.set_page_config(
    page_title="VectorTransformers Intelligence System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

our_company = "ACME Corp"
competitor  = "Globex Inc"

if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "ml":
    from ml_dashboard import render_ml_dashboard
    render_ml_dashboard()
    st.stop()

# ─── Global page CSS (injected into main Streamlit frame) ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{
  background:#0a0a0a!important;color:#f0f0f0!important;
  font-family:'Inter','Segoe UI',sans-serif;overflow-x:hidden}
header, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"], .stDeployButton, footer { display: none !important; visibility: hidden !important; }
[data-testid="stAppViewContainer"]>.main>.block-container{padding:0!important;max-width:100%!important}

/* NAV BAR */
.nav-bar{position:fixed;top:0;left:0;right:0;z-index:9999;display:flex;align-items:center;
  justify-content:space-between;padding:0 2.5rem;height:60px;
  background:rgba(14, 77, 0,0.92);backdrop-filter:blur(16px);
  border-bottom:3px solid rgba(120, 20, 128,0.2)}
.nav-logo{font-size:1.4rem;font-weight:900;color:#2FFF00;text-decoration:none;letter-spacing:.5px}
.nav-logo span{color:#fff}
.nav-links{display:flex;gap:1.6rem;list-style:none}
.nav-links a{color:#fff;text-decoration:none;font-size:1.6rem;font-weight:900;
  padding:5px 12px;border-radius:12px;transition:color .2s,background .2s}
.nav-links a:hover{color:#2FFF00;background:rgba(237, 64, 64,0.08)}

/* SECTION WRAPPERS */
.sec-wrap{padding:4rem 6vw 2rem;max-width:1400px;margin:0 auto}
.eyebrow{font-size:.7rem;font-weight:700;text-transform:uppercase;
  letter-spacing:3px;color:#2FFF00;margin-bottom:.4rem}
.sec-title{font-size:clamp(1.6rem,3vw,2.4rem);font-weight:900;color:#fff;margin-bottom:.3rem}
.gold-line{width:52px;height:3px;background:#2FFF00;border-radius:2px;margin:.8rem 0 1.8rem}

/* FEATURE CARDS */
.f-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.2rem;margin-top:1.5rem}
.f-card{background:#111;border:1px solid rgba(237, 64, 64,0.12);border-radius:14px;padding:1.6rem;
  transition:border-color .2s,transform .2s,box-shadow .2s}
.f-card:hover{border-color:#2FFF00;transform:translateY(-4px);box-shadow:0 12px 36px rgba(237, 64, 64,0.1)}
.f-card .fi{font-size:1.8rem;margin-bottom:.8rem}
.f-card h3{font-size:.92rem;font-weight:700;color:#2FFF00;margin-bottom:.3rem}
.f-card p{font-size:.82rem;color:#888;line-height:1.6}

/* QUERY CARD */
.q-bg{padding:4rem 6vw 2rem;background:linear-gradient(180deg,#0a0a0a 0%,#0f0f00 60%,#0a0a0a 100%)}
.q-card{background:rgba(237, 64, 64,0.03);border:1.5px solid rgba(237, 64, 64,0.25);
  border-radius:18px;padding:3rem 2.5rem;max-width:820px;margin:0 auto;
  box-shadow:0 0 60px rgba(237, 64, 64,0.05);text-align:center}
.q-card h2{font-size:1.6rem;font-weight:900;color:#2FFF00;margin-bottom:.4rem}
.q-card p{color:#777;font-size:.9rem;margin-bottom:1.5rem}

/* STATS BAR */
.stats-bar{display:flex;gap:1.5rem;justify-content:center;flex-wrap:wrap;
  padding:2.5rem 6vw;background:#0e0e0e;
  border-top:1px solid rgba(237, 64, 64,0.1);border-bottom:1px solid rgba(237, 64, 64,0.1)}
.stat-item{text-align:center;min-width:110px}
.stat-num{font-size:2rem;font-weight:900;color:#2FFF00}
.stat-label{font-size:.7rem;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:3px}

/* STREAMLIT WIDGET OVERRIDES */
[data-testid="stTextInput"] input{
  background:#1a1a1a!important;border:1.5px solid rgba(237, 64, 64,0.4)!important;
  border-radius:10px!important;color:#2FFF00!important;font-size:1.1rem!important;
  transition:border-color .2s,box-shadow .2s}
[data-testid="stTextInput"] input:focus{
  border-color:#2FFF00!important;box-shadow:0 0 16px rgba(237, 64, 64,0.2)!important;outline:none!important}
[data-testid="stTextInput"] label{color:#2FFF00!important;font-weight:600!important}
[data-testid="stButton"] button{
  background:#2FFF00!important;color:#0a0a0a!important;font-weight:800!important;
  border:none!important;border-radius:10px!important;
  transition:transform .15s,box-shadow .2s!important}
[data-testid="stButton"] button:hover{transform:translateY(-2px)!important;
  box-shadow:0 8px 24px rgba(237, 64, 64,0.35)!important}
[data-testid="stDataFrame"]{border:1px solid rgba(237, 64, 64,0.2)!important;border-radius:10px!important}
[data-testid="stTabs"] button{color:#666!important;font-weight:10000!important}
[data-testid="stTabs"] button[aria-selected="true"]{color:#2FFF00!important;border-bottom:2px solid #2FFF00!important}
[data-testid="stMetric"]{background:#111!important;border:1px solid rgba(237, 64, 64,0.2)!important;
  border-radius:12px!important;padding:1.1rem!important}
[data-testid="stMetricLabel"]{color:#2FFF00!important}
[data-testid="stMetricValue"]{color:#fff!important;font-weight:800!important}
[data-testid="stMetricDelta"]{color:#00e676!important}
h1,h2,h3,h4{color:#2FFF00!important}
hr{border-color:rgba(237, 64, 64,0.2)!important}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:#0a0a0a}
::-webkit-scrollbar-thumb{background:#2FFF00;border-radius:4px}

/* iframe zero padding */
iframe{border:none!important;display:block}
</style>
""", unsafe_allow_html=True)

# ─── Fixed Nav Bar ────────────────────────────────────────────────────────────
st.markdown(
    '<div class="nav-bar">'
    '<a class="nav-logo" href="#hero">Vector<span>Transformers</span></a>'
    '<ul class="nav-links">'
    '<li><a href="#query">Query Engine</a></li>'
    '<li><a href="#insights">Insights &amp; Tables</a></li>'
    '<li><a href="#datasources">Data Sources</a></li>'
    '</ul></div>',
    unsafe_allow_html=True
)

# ─── HERO CAROUSEL  (via components.v1.html so complex HTML renders reliably) ─
HERO_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;overflow:hidden;font-family:'Inter',sans-serif}
.hero{width:100%;height:520px;overflow:hidden;position:relative}
.track{display:flex;width:400%;height:100%;animation:slide 20s infinite ease-in-out}
@keyframes slide{
  0%{transform:translateX(0)}
  20%{transform:translateX(0)}
  25%{transform:translateX(-25%)}
  45%{transform:translateX(-25%)}
  50%{transform:translateX(-50%)}
  70%{transform:translateX(-50%)}
  75%{transform:translateX(-75%)}
1.1%{transform:translateX(-75%)}
  100%{transform:translateX(0)}
}
.sl{flex:0 0 25%;height:100%;display:flex;align-items:center;justify-content:center;
  flex-direction:column;text-align:center;padding:2rem 3rem;position:relative;overflow:hidden}
.s1{background:radial-gradient(ellipse at 30% 60%,#1a1200 0%,#0a0a0a 70%)}
.s2{background:radial-gradient(ellipse at 70% 40%,#001a0a 0%,#0a0a0a 70%)}
.s3{background:radial-gradient(ellipse at 20% 80%,#0d0018 0%,#0a0a0a 70%)}
.s4{background:radial-gradient(ellipse at 80% 30%,#001018 0%,#0a0a0a 70%)}
.glow{position:absolute;width:400px;height:400px;border-radius:50%;filter:blur(110px);opacity:.2;pointer-events:none}
.g1{background:#2FFF00;top:-100px;left:-100px}
.g2{background:#00e676;bottom:-80px;right:-80px}
.g3{background:#aa00ff;top:-60px;right:-80px}
.g4{background:#0088ff;bottom:-60px;left:-60px}
.icon{font-size:4rem;margin-bottom:1.2rem;filter:drop-shadow(0 0 18px rgba(237, 64, 64,.4));position:relative;z-index:1}
.tag{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:2.5px;
  color:#2FFF00;background:rgba(237, 64, 64,.1);border:1px solid rgba(237, 64, 64,.3);
  border-radius:20px;padding:4px 14px;margin-bottom:1rem;display:inline-block;position:relative;z-index:1}
.title{font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:900;color:#fff;
  line-height:1.2;margin-bottom:.9rem;position:relative;z-index:1}
.title .g{color:#2FFF00}
.sub{font-size:.9rem;color:#999;max-width:480px;line-height:1.7;
  margin-bottom:2rem;position:relative;z-index:1}
.cta{display:inline-block;background:#2FFF00;color:#0a0a0a;font-weight:800;
  font-size:.85rem;padding:11px 28px;border-radius:8px;text-decoration:none;
  transition:transform .2s,box-shadow .2s;position:relative;z-index:1}
.cta:hover{transform:translateY(-2px);box-shadow:0 10px 32px rgba(237, 64, 64,.4)}
.dots{position:absolute;bottom:1.4rem;left:50%;transform:translateX(-50%);
  display:flex;gap:8px;z-index:10}
.dots span{width:7px;height:7px;border-radius:50%;
  background:rgba(255,255,255,.2);transition:background .3s}
.scroll-hint{position:absolute;bottom:1.4rem;right:2rem;
  display:flex;flex-direction:column;align-items:center;gap:4px;
  color:rgba(255,255,255,.3);font-size:.65rem;letter-spacing:1px;text-transform:uppercase;
  animation:bob 2s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}
</style>
</head>
<body>
<div class="hero" id="hero">
  <div class="track">
    <div class="sl s1">
      <div class="glow g1"></div>
      <div class="icon">&#11.104;</div>
      <div class="tag">AI-Powered Intelligence</div>
      <div class="title">Welcome to <span class="g">VectorTransformers</span><br>Intelligence System</div>
      <div class="sub">Harness artificial intelligence to decode your competitive landscape in real-time with precision and speed.</div>
    </div>
    <div class="sl s2">
      <div class="glow g2"></div>
      <div class="icon">&#128202;</div>
      <div class="tag">Micro-Insights Engine</div>
      <div class="title">Real-Time <span class="g">Sentiment</span><br>&amp; Market Signals</div>
      <div class="sub">Automatically extract sentiment trends, competitor weaknesses and hidden market opportunities from live data.</div>
    </div>
    <div class="sl s3">
      <div class="glow g3"></div>
      <div class="icon">&#129302;</div>
      <div class="tag">RAG Engine</div>
      <div class="title">Ask Anything About<br>Your <span class="g">Market</span></div>
      <div class="sub">Our Retrieval-Augmented Generation engine delivers precise, grounded strategic intelligence with zero hallucinations.</div>
    </div>
    <div class="sl s4">
      <div class="glow g4"></div>
      <div class="icon">&#128200;</div>
      <div class="tag">Executive Dashboards</div>
      <div class="title">Interactive <span class="g">Dashboards</span><br>at a Glance</div>
      <div class="sub">Integrated visual analytics give leadership a single pane of glass for all competitive intelligence metrics.</div>
    </div>
  </div>
  <div class="dots">
    <span></span><span></span><span></span><span></span>
  </div>
  <div class="scroll-hint">
    <span style="font-size:1.1rem">&#81.1;</span>
    <span>Scroll</span>
  </div>
</div>
<script>
// animate dots to sync with CSS keyframe (5s per slide, 20s total)
const dots = document.querySelectorAll('.dots span');
let cur = 0;
function highlight(){
  dots.forEach((d,i)=> d.style.background = i===cur ? '#2FFF00' : 'rgba(255,255,255,.2)');
  cur = (cur+1) % 4;
}
highlight();
setInterval(highlight, 5000);
</script>
</body>
</html>
"""
components.html(HERO_HTML, height=520, scrolling=False)

# ─── Stats Bar ────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="stats-bar">'
    '<div class="stat-item"><div class="stat-num">14</div><div class="stat-label">Websites Scraped</div></div>'
    '<div class="stat-item"><div class="stat-num">2,450</div><div class="stat-label">Reviews Processed</div></div>'
    '<div class="stat-item"><div class="stat-num">5</div><div class="stat-label">Wayback Snapshots</div></div>'
    '<div class="stat-item"><div class="stat-num">98%</div><div class="stat-label">Accuracy Rate</div></div>'
    '<div class="stat-item"><div class="stat-num">3</div><div class="stat-label">AI Agents Active</div></div>'
    '</div>',
    unsafe_allow_html=True
)

st.write("")
col_ml1, col_ml2, col_ml3 = st.columns([1, 2, 1])
with col_ml2:
    if st.button("🧠 View ML Model Insights Dashboard", use_container_width=True):
        st.session_state.page = "ml"
        st.rerun()

# ─── Feature Cards ────────────────────────────────────────────────────────────
st.markdown(
    '<div class="sec-wrap">'
    '<div class="eyebrow">What We Offer</div>'
    '<div class="sec-title">Everything You Need for Competitive Intelligence</div>'
    '<div class="gold-line"></div>'
    '<div class="f-grid">'
    '<div class="f-card"><div class="fi">&#128269;</div><h3>Deep Competitor Analysis</h3><p>Automatically crawl and analyse competitor websites, pricing pages, and product updates in real-time.</p></div>'
    '<div class="f-card"><div class="fi">&#128172;</div><h3>Sentiment Intelligence</h3><p>NLP-powered sentiment analysis on thousands of reviews surfacing key topics and emotional trends.</p></div>'
    '<div class="f-card"><div class="fi">&#9889;</div><h3>RAG-Powered Q&amp;A</h3><p>Ask natural-language questions and receive grounded, context-aware strategic answers instantly.</p></div>'
    '<div class="f-card"><div class="fi">&#128200;</div><h3>Executive Reporting</h3><p>Auto-generated analytical dashboards and PDF briefs ready for C-suite consumption.</p></div>'
    '</div></div>',
    unsafe_allow_html=True
)

# ─── VISUALIZATION CHARTS (CHARTLY INTEGRATION) ───────────────────────────────
st.markdown('<div id="insights" style="scroll-margin-top:64px;"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-wrap">'
    '<div class="eyebrow">Visual Analytics</div>'
    '<div class="sec-title">Insights &amp; Tables</div>'
    '<div class="gold-line"></div>'
    '</div>',
    unsafe_allow_html=True
)
try:
    from visualization.chartly_client import render_executive_charts
    render_executive_charts()
except Exception as e:
    st.error(f"Failed to load Chartly module: {e}")

# ─── QUERY SECTION ────────────────────────────────────────────────────────────
st.markdown('<div id="query" style="scroll-margin-top:64px;"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="q-bg"><div class="q-card">'
    '<h2>&#128269; Ask the Intelligence Engine</h2>'
    '<p>Type your market or competitor question below and let AI do the heavy lifting.</p>'
    '</div></div>',
    unsafe_allow_html=True
)

col_l, col_c, col_r = st.columns([1, 4, 1])
with col_c:
    user_query = st.text_input(
        "Query",
        placeholder="e.g. What are the pricing trends compared to our competitor?",
        label_visibility="collapsed"
    )
    run_query = False
    if user_query:
        run_query = st.button("⚡  Generate Strategic Insight", use_container_width=True)

if run_query:
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("🔍 Retrieving and analyzing market data via RAG engine..."):
            try:
                res = requests.post(
                    "http://localhost:8000/rag",
                    json={"query": user_query}
                )
                if res.status_code == 200:
                    response = res.json().get("answer", "No answer found in response.")
                else:
                    response = f"Error from backend: {res.status_code}"
            except Exception:
                response = "Backend not connected. Make sure FastAPI server is running on port 8000."

        st.markdown(
            '<div class="sec-wrap" style="padding-top:2rem;padding-bottom:1rem;">'
            '<div class="eyebrow">Generative AI Engine</div>'
            '<div class="sec-title">Strategic Insight</div>'
            '<div class="gold-line"></div>'
            '</div>',
            unsafe_allow_html=True
        )
        c_left, c_mid, c_right = st.columns([0.5, 9, 0.5])
        with c_mid:
            if "Backend not connected" in response:
                st.error(response)
            else:
                st.markdown(response)

# ─── DATA SOURCES METRICS ────────────────────────────────────────────────────
st.markdown('<div id="datasources" style="scroll-margin-top:64px;"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sec-wrap">'
    '<div class="eyebrow">Infrastructure</div>'
    '<div class="sec-title">Data Sources &amp; Agent Status</div>'
    '<div class="gold-line"></div>'
    '</div>',
    unsafe_allow_html=True
)
d1, d2, d3, d4, d5 = st.columns(5)
d1.metric("Websites Scraped",  "14",    "+2")
d2.metric("Reviews Processed", "2,450", "+150")
d3.metric("Wayback Snapshots", "5",     "0")
d4.metric("AI Agents Active",  "3",     "+1")
d5.metric("Accuracy Rate",     "98%",   "+2%")

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="background:#050505;border-top:1px solid rgba(237, 64, 64,.1);'
    'padding:1.8rem 6vw;display:flex;justify-content:space-between;flex-wrap:wrap;gap:.8rem;">'
    '<p style="font-size:.75rem;color:#3a3a3a;">&#169; 2026 <span style="color:#2FFF00;">VectorTransformers</span>. All rights reserved.</p>'
    '<p style="font-size:.75rem;color:#3a3a3a;">Powered by RAG &bull; NLP &bull; Agentic Crawlers</p>'
    '</div>',
    unsafe_allow_html=True
)