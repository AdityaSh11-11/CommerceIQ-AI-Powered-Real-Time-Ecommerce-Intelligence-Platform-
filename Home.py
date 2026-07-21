import streamlit as st
from sqlalchemy import create_engine, text
from config import DATABASE_URL

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="CommerceIQ",
    page_icon="🛒",
    layout="wide"
)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
engine = create_engine(DATABASE_URL)


def database_status():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except:
        return False


# ==========================================================
# HERO
# ==========================================================

st.markdown("""
<div class="hero">

<h1>
🛒 CommerceIQ
</h1>

<h2>
AI-Powered Real-Time Ecommerce Intelligence Platform
</h2>

<p>
Transforming E-Commerce Data into Real-Time Intelligence, Predictive Insights & Autonomous Business Decisions
</p>


</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# PLATFORM STATUS
# ==========================================================

st.markdown("""
<h2 class="section-title">
Platform Status
</h2>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:

    if database_status():
        status = "🟢 ONLINE"
    else:
        status = "🔴 OFFLINE"

    st.markdown(f"""
    <div class="metric">

    <h4>Database</h4>

    <h2>{status}</h2>

    PostgreSQL Connected

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="metric">

    <h4>AI Engine</h4>

    <h2>ACTIVE</h2>

    Gemini AI Ready

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown("""
    <div class="metric">

    <h4>Forecast Engine</h4>

    <h2>READY</h2>

    ML Models Loaded

    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================================
# CAPABILITIES
# ==========================================================

st.markdown("""
<h2 class="section-title">
Platform Capabilities
</h2>
""", unsafe_allow_html=True)

cards = [

("Business Intelligence",
"Interactive dashboards, KPI monitoring, customer insights and executive reporting."),

("Real-Time Analytics",
"Monitor transactions, revenue growth and operational metrics in real time."),

("Artificial Intelligence",
"LLM powered recommendations, anomaly detection and automated business insights."),

("Machine Learning",
"Sales forecasting, demand prediction, customer segmentation and churn prediction.")

]

cols = st.columns(4)

for col, card in zip(cols, cards):

    with col:

        st.markdown(f"""
        <div class="feature">

        <h3>{card[0]}</h3>

        <br>

        <p>{card[1]}</p>

        </div>
        """, unsafe_allow_html=True)

st.write("")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""
<br><br>

<div class="footer">

<h3>
🛒 CommerceIQ
</h3>

<p>
AI-Powered Commerce Intelligence Platform
</p>

<div class="footer-links">

<span>Real-Time Analytics</span>
&nbsp; • &nbsp;
<span>Predictive Intelligence</span>
&nbsp; • &nbsp;
<span>Business Automation</span>

</div>

<br>

<p class="copyright">
© 2026 CommerceIQ. Built by Aditya Sharma
</p>

</div>

""", unsafe_allow_html=True)