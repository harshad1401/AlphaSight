import streamlit as st

# PAGE CONFIGURATION -
st.set_page_config(
    page_title="TradeVision",
    page_icon="heavy_dollar_sign:",
    layout="wide"
)

# CUSTOM CSS -
st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* ================= HEADER ================= */

.tradevision-header {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 45px 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 40px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
}

.tradevision-header h1 {
    color: white !important;
    font-size: 52px !important;
    font-weight: 700 !important;
    margin: 0 0 12px 0 !important;
}

.tradevision-header h2 {
    color: white !important;
    font-size: 24px !important;
    font-weight: 400 !important;
    margin: 0 0 15px 0 !important;
}

.tradevision-header p {
    color: #eeeeee !important;
    font-size: 18px !important;
    margin: 0 !important;
}

/* ================= SERVICES TITLE ================= */

.services-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #203a43;
    margin: 30px 0;
}

/* ================= SERVICE CARDS ================= */

.service-card {
    background-color: #f5f7fa;
    border: 1px solid #d9dee3;
    border-radius: 18px;
    padding: 25px;
    min-height: 220px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.service-card:hover {
    transform: translateY(-10px);
    background-color: white;
    border-color: #2c5364;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.18);
}

.service-card h3 {
    color: #203a43 !important;
    font-size: 22px;
    margin-bottom: 15px;
}

.service-card p {
    color: #555555 !important;
    font-size: 16px;
    line-height: 1.6;
}

/* ================= BUTTONS ================= */

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #203a43;
    background-color: white;
    color: #203a43;
    font-weight: 600;
    padding: 10px;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #203a43;
    color: white;
    border-color: #203a43;
    transform: scale(1.03);
}

/* ================= ABOUT ================= */

.about-section {
    margin-top: 45px;
    padding: 30px;
    border-radius: 18px;
    background-color: #f5f7fa;
    border: 1px solid #d9dee3;
    text-align: center;
}

.about-section h2 {
    color: #203a43 !important;
    font-size: 28px;
}

.about-section p {
    color: #555555 !important;
    font-size: 17px;
    line-height: 1.7;
}

/* ================= FOOTER ================= */

.tradevision-footer {
    margin-top: 60px;
    padding: 30px;
    text-align: center;
    border-top: 1px solid #dddddd;
}

.tradevision-footer h3 {
    color: #203a43 !important;
    font-size: 22px;
}

.tradevision-footer p {
    color: #777777 !important;
    font-size: 14px;
    margin: 5px;
}

</style>
""", unsafe_allow_html=True)

# HEADER -
st.markdown("""
<div class="tradevision-header">
<h1>📈 TradeVision</h1>
<h2>Intelligent Stock Market Analysis, Prediction & Risk Assessment Platform</h2>
<p>Analyze Markets. Predict Trends. Manage Risk.</p>
</div>
""", unsafe_allow_html=True)

# SERVICES TITLE -
st.markdown(
    '<div class="services-title">🚀 Explore Our Services</div>',
    unsafe_allow_html=True
)

# SERVICE COLUMNS -
col1, col2, col3, col4 = st.columns(4)

# STOCK ANALYSIS -

with col1:

    st.markdown("""
<div class="service-card">
<h3>📊 Stock Analysis</h3>
<p>
Analyze stock prices, historical trends, daily returns
and important market indicators to understand stock performance.
</p>
</div>
""", unsafe_allow_html=True)

    st.write("")

    if st.button("Explore Analysis →", key="analysis"):
        st.switch_page("pages/Stock_Analysis.py")


# ============================================================
# STOCK PREDICTION
# ============================================================

with col2:

    st.markdown("""
<div class="service-card">
<h3>🔮 Stock Prediction</h3>
<p>
Forecast future stock prices using historical market
data and advanced forecasting models.
</p>
</div>
""", unsafe_allow_html=True)

    st.write("")

    if st.button("Explore Prediction →", key="prediction"):
        st.switch_page("pages/Stock_Prediction.py")


# ============================================================
# CAPM RETURN
# ============================================================

with col3:

    st.markdown("""
<div class="service-card">
<h3>📈 CAPM Return</h3>
<p>
Calculate the expected return of a stock using the
Capital Asset Pricing Model based on market risk and performance.
</p>
</div>
""", unsafe_allow_html=True)

    st.write("")

    if st.button("Calculate Return →", key="capm_return"):
        st.switch_page("pages/CAPM_Return.py")


# ============================================================
# CAPM BETA
# ============================================================

with col4:

    st.markdown("""
<div class="service-card">
<h3>⚖️ CAPM Beta</h3>
<p>
Measure a stock's systematic risk and sensitivity
compared with the overall market using Beta.
</p>
</div>
""", unsafe_allow_html=True)

    st.write("")

    if st.button("Calculate Beta →", key="capm_beta"):
        st.switch_page("pages/Calculate_Beta.py")


# ============================================================
# ABOUT TRADEVISION
# ============================================================

st.markdown("""
<div class="about-section">
<h2>💡 About TradeVision</h2>

<p>
TradeVision is an intelligent stock market analysis platform
designed to help users understand market trends, analyze stock
performance, forecast future prices and evaluate investment risk.
</p>

<p>
The platform combines historical market data, time-series
forecasting and financial models such as CAPM and Beta to provide
useful investment insights.
</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="tradevision-footer">
<h3>📈 TradeVision</h3>

<p>
Analyze Markets. Predict Trends. Manage Risk.
</p>

<p>
Intelligent Stock Market Analysis, Prediction & Risk Assessment Platform
</p>

<p>
© 2026 TradeVision | All Rights Reserved
</p>
</div>
""", unsafe_allow_html=True)