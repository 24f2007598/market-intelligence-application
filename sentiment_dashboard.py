import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.db import engine

def fetch_sentiment_metrics():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT sentiment_label, COUNT(*) FROM reviews WHERE sentiment_label IS NOT NULL GROUP BY sentiment_label")).fetchall()
        
        # Recent negative reviews
        bad_revs = conn.execute(text("SELECT company, review_text, sentiment_score FROM reviews WHERE sentiment_label = 'negative' ORDER BY id DESC LIMIT 5")).fetchall()
        
    dist = {r[0]: r[1] for r in res}
    bad = [{"Company": r[0], "Review": r[1], "Confidence": f"{r[2]*100:.1f}%"} for r in bad_revs]
    return dist, bad

def render_sentiment_dashboard():
    # Hide default headers
    st.markdown("""
        <style>
        [data-testid="stAppViewBlockContainer"] { padding-top: 0rem; }
        header { visibility: hidden; }
        .stButton>button { background: #2FFF00 !important; color: #fff !important; font-weight: 800; border-radius: 8px; border: none; }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = "main"
            st.rerun()
            
    with col2:
        st.markdown("<h2 style='color:#2FFF00;'>Analyst Sentiment Layer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#aaa;'>Real-time AI RoBERTa classifications on global reviews</p>", unsafe_allow_html=True)

    dist, bad_revs = fetch_sentiment_metrics()
    
    st.markdown("### 📊 Live Sentiment Distribution")
    c1, c2, c3 = st.columns(3)
    c1.metric("Positive 🟢", dist.get('positive', 0))
    c2.metric("Neutral ⚪", dist.get('neutral', 0))
    c3.metric("Negative 🔴", dist.get('negative', 0))

    st.markdown("---")
    st.markdown("### 🚨 High-Priority Negative Signals")
    if bad_revs:
        df = pd.DataFrame(bad_revs)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No negative reviews detected or sentiment pipeline still processing!")
