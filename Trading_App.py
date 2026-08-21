# Import libraries -
import streamlit as st

# PAGE CONFIGURATION -
st.set_page_config(
    page_title="AlphaSight",
    page_icon="heavy_dollar_sign:",
    layout="wide"
)

# CUSTOM CSS -
st.markdown("""
<style>

.stApp {
    background-color: #131722;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* ================= HEADER ================= */

.alphasight-header {
    padding: 45px;
    border-radius: 12px;
    text-align: center;
    color: #F0F3FA;
    margin-bottom: 40px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    background: #1E222D;
    border: 1px solid #363A45;
}

.alphasight-header h1 {
    font-size: 52px !important;
    font-weight: 700 !important;
    margin: 0 0 15px 0 !important;
    cursor: pointer;
    text-shadow: 6px 6px 8px rgba(0,0,0,0.5);
}

.alphasight-header h2 {
    color: #D1D4DC !important;
    font-size: 24px !important;
    font-weight: 400 !important;
    margin: 0 0 15px 0 !important;
}

.alphasight-header p {
    color: #787B86 !important;
    font-size: 18px !important;
    margin: 0 !important;
}

/* ================= SERVICES TITLE ================= */

.services-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #F0F3FA;
    margin: 30px 0;
}

/* ================= SERVICE CARDS ================= */

.service-card {
    background-color: #1E222D;
    border: 1px solid #363A45;
    border-radius: 10px;
    padding: 25px;
}

.service-card:hover {
    background-color: #2A2E39;
    border-color: #2962FF;
}

.service-card h3 {
    color: #F0F3FA !important;
    font-size: 22px;
    margin-bottom: 15px;
}

.service-card p {
    color: #787B86 !important;
    font-size: 16px;
    line-height: 1.6;
}

/* ================= BUTTONS ================= */

div.stButton > button {
    border-radius: 6px;
    background-color: #393a40;
    color: #F0F3FA;
    font-weight: 600;
    padding: 10px 20PX;
    text-decoration: none;
    display: inline-block;
    border: none;
}

div.stButton > button:hover {
    background-color: #203a43;
    color: white;
    border-color: #203a43;
}

/* ================= ABOUT ================= */

.about-section {
    margin-top: 80px;
    padding: 30px;
    border-radius: 18px;
    background: #1E222D;
    border: 1px solid #363A45;
    text-align: center;
}

.about-section h2 {
    color: #F0F3FA !important;
    font-size: 28px;
}

.about-section p {
    color: #787B86 !important;
    font-size: 17px;
    line-height: 1.7;
}

/* ================= FOOTER ================= */

.alphasight-footer {
    margin-top: 60px;
    padding: 30px;
    text-align: center;
    border-top: 1px solid #dddddd;
}

.alphasight-footer h3 {
    color: #D1D4DC !important;
    font-size: 20px;
}

.alphasight-footer p {
    color: #787B86 !important;
    font-size: 14px;
    margin: 5px;
}

</style>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

# HEADER -
st.markdown("""
<div class="alphasight-header">
<h1>AlphaSight</h1>
<h2>Intelligent Stock Analytics & Investment Insights</h2>
<p>Smart Investment Planning & Risk Assessment Platform</p>
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

# STOCK PREDICTION -
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

# CAPM RETURN -
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

# CAPM BETA -
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

# ABOUT ALPHASIGHT -
st.markdown("""
<div class="about-section">
<h2>💡 About AlphaSight</h2>

<p>
AlphaSight is an intelligent Stock Market Analysis and Prediction platform designed to help users make Data-Driven Investment Decisions.
</p>

<p>
It integrates Historical Market Data, Risk Analysis, CAPM, Beta, 
Expected Return Calculations, and Time-Series Forecasting to evaluate Investment Opportunities.
It is designed to help users interpret complex market information efficiently and make Investment Decisions based on Analytical Evidence rather than assumptions.
</p>
</div>
""", unsafe_allow_html=True)

# FOOTER -
st.markdown("""
<div class="alphasight-footer">
<h3>◈ AlphaSight</h3>

<p>Transforming Market Data into Actionable Investment Insights</p>

<p>See the Market. Know the Risk.</p>

<p>Select Market Data Provided by <a href="https://finance.yahoo.com" style="color: #4d79ff; text-decoration: none;">YahooFinance</a>.</p>

<p>© 2026 alphasight | All Rights Reserved</p>

<a href="https://www.instagram.com" target="_blank" class="fa fa-instagram" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.facebook.com" target="_blank" class="fa fa-facebook" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.twitter.com" target="_blank" class="fa fa-twitter" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.youtube.com" target="_blank" class="fa fa-youtube" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.telegram.com" target="_blank" class="fa fa-telegram" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.reddit.com" target="_blank" class="fa fa-reddit" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a>
</div>
""", unsafe_allow_html=True)
