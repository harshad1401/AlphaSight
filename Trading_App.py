# Import libraries -
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import textwrap

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
        background-color: #0B0F14;
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
        color: #F5F7FA;
        margin-bottom: 40px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        background: #121820;
        border: 1px solid #26313D;
    }

    .alphasight-header h1 {
        font-size: 52px !important;
        font-weight: 700 !important;
        margin: 0 0 15px 0 !important;
        cursor: pointer;
        text-shadow: 6px 6px 8px rgba(0,0,0,0.5);
    }

    .alphasight-header h2 {
        color: #C7D0DA !important;
        font-size: 24px !important;
        font-weight: 400 !important;
        margin: 0 0 15px 0 !important;
    }

    .alphasight-header p {
        color: #8B98A8 !important;
        font-size: 16px !important;
        margin: 0 !important;
    }


    /* ================ ALPHASIGHT MARKET SCORE ( START ) ==================  */

    .alpha-score-card {
        background-color: #121820;

        border: 1px solid #26313D;

        border-radius: 14px;

        padding: 25px 28px;

        margin-top: 15px;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.25);
    }

    /* ====================== Title ======================= */

    .score-title {
        font-size: 14px;

        font-weight: 700;

        color: #8B98A8;

        letter-spacing: 1px;
    }

    /* Main score */

    .score-value {
        font-size: 54px;

        font-weight: 800;

        color: #f5f7fa;

        margin-top: 8px;
    }

    .score-value span {
        font-size: 20px;

        color: #8B98A8;

        font-weight: 500;
    }

    /* ================== Condition ====================== */

    .score-condition {
        font-size: 16px;

        font-weight: 600;

        margin-bottom: 25px;

        color: #26a69a;
    }

    /* ================= Metric row ================= */

    .score-row {
        display: grid;

        grid-template-columns:
            110px
            1fr
            35px;

        align-items: center;

        gap: 10px;

        margin: 13px 0;

        font-size: 13px;

        color: #8B98A8;
    }

    /* =================== Progress bar ==================== */

    .progress {
        height: 6px;

        background: #252b32;

        border-radius: 10px;

        overflow: hidden;
    }

    .progress div {
        height: 100%;

        background: #26a69a;

        border-radius: 10px;
    }

    /* ================== Score number ================== */

    .score-row b {
        color: #e8eaed;

        text-align: right;
    }

    /* ====================== Footer =================== */

    .score-footer {
        margin-top: 22px;

        padding-top: 13px;

        border-top: 1px solid #26313D;

        font-size: 11px;

        color: #68717c;
    }
    
    /* ================ ALPHASIGHT MARKET SCORE ( END ) ==================  */

    /* ================= SERVICES TITLE ================= */

    .services-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        color: #F5F7FA;
        margin: 30px 0;
    }

    /* ================= SERVICE CARDS ================= */

    .service-card {
        background-color: #121820;
        border: 1px solid #26313D;
        border-radius: 10px;
        padding: 25px;
    }

    .service-card:hover {
        background-color: #171F29;
        border-color: #26313D;
    }

    .service-card h3 {
        color: #C7D0DA !important;
        font-size: 22px;
        margin-bottom: 15px;
    }

    .service-card p {
        color: #8B98A8 !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* ================= BUTTONS ================= */

    div.stButton > button {
        border-radius: 6px;
        background-color: #171F29;
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
        background: #121820;
        border: 1px solid #26313D;
        text-align: center;
    }

    .about-section h2 {
        color: #F5F7FA !important;
        font-size: 28px;
    }

    .about-section p {
        color: #8B98A8 !important;
        font-size: 15px;
        line-height: 1.7;
    }

    /* ================= FOOTER ================= */

    .alphasight-footer {
        margin-top: 60px;
        padding: 30px;
        text-align: center;
        border-top: 1px solid #26313D;
    }

    .alphasight-footer h3 {
        color: #D1D4DC !important;
        font-size: 20px;
    }

    .alphasight-footer p {
        color: #8B98A8 !important;
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
<p>See the Market • Measure the Risk • Discover the Opportunity</p>
</div>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def calculate_market_score():

    # S&P 500 DATA -
    sp500 = yf.download(
        "^GSPC",
        period="6mo",
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if sp500.empty:
        return None

    close = sp500["Close"]

    # Handle yfinance MultiIndex
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    close = close.dropna()

    # 1. MOMENTUM SCORE -
    return_20d = (
        (close.iloc[-1] / close.iloc[-21]) - 1
    ) * 100

    # Convert return to score
    momentum_score = np.clip(
        50 + (return_20d * 10),
        0,
        100
    )

    # 2. VOLATILITY SCORE -
    vix = yf.download(
        "^VIX",
        period="1mo",
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if not vix.empty:

        vix_close = vix["Close"]

        if isinstance(vix_close, pd.DataFrame):
            vix_close = vix_close.iloc[:, 0]

        vix_value = float(vix_close.dropna().iloc[-1])

        # Lower VIX = better score
        volatility_score = np.clip(
            100 - ((vix_value - 10) * 4),
            0,
            100
        )

    else:
        vix_value = 20
        volatility_score = 50

    # 3. BREADTH SCORE -
    sma_20 = close.rolling(20).mean()

    breadth_score = (
        70
        if close.iloc[-1] > sma_20.iloc[-1]
        else 40
    )

    # 4. TREND SCORE -
    sma_50 = close.rolling(50).mean()
    sma_200 = close.rolling(200).mean()

    current_price = float(close.iloc[-1])
    ma50 = float(sma_50.iloc[-1])
    ma200 = float(sma_200.iloc[-1])

    trend_score = 50

    if current_price > ma50:
        trend_score += 20

    if current_price > ma200:
        trend_score += 20

    if ma50 > ma200:
        trend_score += 10

    trend_score = np.clip(
        trend_score,
        0,
        100
    )

    # FINAL SCORE -
    market_score = (
        momentum_score * 0.30
        + volatility_score * 0.20
        + breadth_score * 0.25
        + trend_score * 0.25
    )

    market_score = round(
        float(market_score),
        1
    )

    # MARKET CONDITION -
    if market_score >= 80:
        condition = "Strong Bullish"
        icon = "🟢"

    elif market_score >= 65:
        condition = "Bullish"
        icon = "🟢"

    elif market_score >= 50:
        condition = "Neutral"
        icon = "🟡"

    elif market_score >= 35:
        condition = "Bearish"
        icon = "🔴"

    else:
        condition = "Strong Bearish"
        icon = "🔴"

    return {
        "score": market_score,
        "condition": condition,
        "icon": icon,
        "momentum": round(float(momentum_score)),
        "volatility": round(float(volatility_score)),
        "breadth": round(float(breadth_score)),
        "trend": round(float(trend_score)),
        "vix": round(vix_value, 2)
    }
    
# ALPHASIGHT MARKET SCORE -
score_data = calculate_market_score()

if score_data:

    score_html = f"""
    <div class="alpha-score-card">

        <div class="score-title">
            🧠 ALPHASIGHT MARKET SCORE
        </div>

        <div class="score-value">
            {score_data["score"]:.0f}
            <span>/ 100</span>
        </div>

        <div class="score-condition">
            {score_data["icon"]}
            {score_data["condition"]}
        </div>

        <div class="score-row">
            <span>📈 Momentum</span>

            <div class="progress">
                <div style="width: {score_data["momentum"]}%;"></div>
            </div>

            <b>{score_data["momentum"]}</b>
        </div>

        <div class="score-row">
            <span>⚡ Volatility</span>

            <div class="progress">
                <div style="width: {score_data["volatility"]}%;"></div>
            </div>

            <b>{score_data["volatility"]}</b>
        </div>

        <div class="score-row">
            <span>📊 Breadth</span>

            <div class="progress">
                <div style="width: {score_data["breadth"]}%;"></div>
            </div>

            <b>{score_data["breadth"]}</b>
        </div>

        <div class="score-row">
            <span>📉 Trend</span>

            <div class="progress">
                <div style="width: {score_data["trend"]}%;"></div>
            </div>

            <b>{score_data["trend"]}</b>
        </div>

        <div class="score-footer">
            VIX: {score_data["vix"]}
            &nbsp; • &nbsp;
            Updated automatically
        </div>

    </div>
    """
    
    # IMPORTANT: use st.html()
    st.html(score_html)

# SERVICES TITLE -
st.markdown(
    '<div class="services-title">🚀 Explore Our Services</div>',
    unsafe_allow_html=True
)

# SERVICE COLUMNS -
col1, col2, col3, col4 = st.columns(4)

# STOCK ANALYSIS -
with col1:

    st.html("""
        <div class="service-card">
            <h3>📊 Stock Analysis</h3>
            <p>
                Analyze stock prices, historical trends, daily returns
                and important market indicators to understand stock performance.
            </p>
        </div>
    """)

    st.write("")

    if st.button("Explore Analysis →", key="analysis"):
        st.switch_page("pages/Stock_Analysis.py")

# STOCK PREDICTION -
with col2:

    st.html("""
        <div class="service-card">
        <h3>🔮 Stock Prediction</h3>
        <p>
        Forecast future stock prices using historical market
        data and advanced forecasting models.
        </p>
        </div>
    """)

    st.write("")

    if st.button("Explore Prediction →", key="prediction"):
        st.switch_page("pages/Stock_Prediction.py")

# CAPM RETURN -
with col3:

    st.html("""
        <div class="service-card">
        <h3>📈 CAPM Return</h3>
        <p>
        Calculate the expected return of a stock using the
        Capital Asset Pricing Model based on market risk and performance.
        </p>
        </div>
    """)

    st.write("")

    if st.button("Calculate Return →", key="capm_return"):
        st.switch_page("pages/CAPM_Return.py")

# CAPM BETA -
with col4:

    st.html("""
    <div class="service-card">
    <h3>⚖️ CAPM Beta</h3>
    <p>
    Measure a stock's systematic risk and sensitivity
    compared with the overall market using Beta.
    </p>
    </div>
    """)

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

<p>See the Market • Measure the Risk • Discover the Opportunity</p>

<p>Select Market Data Provided by <a href="https://finance.yahoo.com" style="color: #4d79ff; text-decoration: none;">YahooFinance</a>.</p>

<p>© 2026 AlphaSight | All Rights Reserved</p>

<a href="https://www.instagram.com" target="_blank" class="fa fa-instagram" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.facebook.com" target="_blank" class="fa fa-facebook" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.twitter.com" target="_blank" class="fa fa-twitter" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.youtube.com" target="_blank" class="fa fa-youtube" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.telegram.com" target="_blank" class="fa fa-telegram" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a> |
<a href="https://www.reddit.com" target="_blank" class="fa fa-reddit" style="font-size: 24px; color: #707079FF; text-decoration: none; margin: 5px;"></a>
</div>
""", unsafe_allow_html=True)
