# Importing libraries -
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta

from pages.utils.plotly_figure import (
    plotly_table,
    candlestick,
    RSI,
    MACD,
    close_chart,
    moving_average
)

# Setting Page Config -
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide"
)

# CUSTOM CSS -
st.markdown("""
<style>

.stApp {
    background-color: white;
}

</style>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

st.title("Stock Analysis")

# Getting Input from User -
col1, col2, col3 = st.columns(3)

# Import Dataset -
sp500 = pd.read_csv("sp500_companies.csv")

# Display Companies -
# st.dataframe(sp500)

# Get ticker list -
tickers_list = sp500['Symbol'].to_list()

today = datetime.date.today()

with col1:
    ticker = st.selectbox("Choose a Stock: ", tickers_list)
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(
        today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(
        today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

try:
    info = stock.info
    summary = info.get("longBusinessSummary")

    if summary:
        st.write(summary)
    else:
        st.info("Business summary is not available for this stock.")

except Exception as e:
    st.error(f"Unable to retrieve stock information: {e}")

st.write("Sector : ", stock.info['sector'])
st.write("Full-Time Employees : ", stock.info['fullTimeEmployees'])
st.write("Website : ", stock.info['website'])

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])

    df[''] = [
        stock.info.get("marketCap", 0),
        stock.info.get("beta", 0),
        stock.info.get("trailingEps", 0),
        stock.info.get("trailingPE", 0)
    ]

    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)
with col2:
    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per Share',
                      'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df[''] = [
        stock.info.get('quickRatio', 0),
        stock.info.get('revenuePerShare', 0),
        stock.info.get('profitMargins', 0),
        stock.info.get('debtToEquity', 0),
        stock.info.get('returnOnEquity', 0)
    ]

    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

try:
    data = yf.download(ticker, start=start_date, end=end_date)

    col1, col2 = st.columns(2)
    if isinstance(data.columns, pd.MultiIndex):
        close_data = data["Close"].iloc[:, 0]
    else:
        close_data = data["Close"]

    close_data = pd.Series(close_data).dropna()

    daily_change = close_data.iloc[-1] - close_data.iloc[-2]

    col1.metric("Current Price", f"{close_data.iloc[-1]:.2f}$")
    col2.metric("Daily Change", f"{daily_change:.2f}%")

    # ================== Historical Data (Last 10 Days) ===================
    last_10_df = (
        data.tail(10)
        .sort_index(ascending=False)
        .round(3)
    )

    if isinstance(last_10_df.columns, pd.MultiIndex):
        last_10_df.columns = last_10_df.columns.get_level_values(0)

    fig_df = plotly_table(last_10_df)

    st.write("##### Historical Data (Last 10 Days)")
    st.plotly_chart(fig_df, use_container_width=True)

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    num_period = ''

    if "num_period" not in st.session_state:
        st.session_state.num_period = "1Y"

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        if st.button("5D", use_container_width=True):
            st.session_state.num_period = "5D"

    with col2:
        if st.button("1M", use_container_width=True):
            st.session_state.num_period = "1M"

    with col3:
        if st.button("6M", use_container_width=True):
            st.session_state.num_period = "6M"

    with col4:
        if st.button("YTD", use_container_width=True):
            st.session_state.num_period = "YTD"

    with col5:
        if st.button("1Y", use_container_width=True):
            st.session_state.num_period = "1Y"

    with col6:
        if st.button("5Y", use_container_width=True):
            st.session_state.num_period = "5Y"

    with col7:
        if st.button("MAX", use_container_width=True):
            st.session_state.num_period = "MAX"

    num_period = st.session_state.num_period

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        chart_type = st.selectbox('', ('Candle', 'Line'))
    with col2:
        if chart_type == 'Candle':
            indicators = st.selectbox('', ('RSI', 'MACD'))
        else:
            indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

    ticker_ = yf.Ticker(ticker)
    data1 = ticker_.history(period='max')
    if data1.empty:
        st.warning("Unable to load chart data.")
    else:

        # ============== CANDLE CHART ==================
        if chart_type == 'Candle':
            st.plotly_chart(
                candlestick(
                    data1,
                    num_period
                ),
                use_container_width=True
            )

            if indicators == 'RSI':
                st.plotly_chart(
                    RSI(
                        data1,
                        num_period
                    ),
                    use_container_width=True
                )

            elif indicators == "MACD":
                st.plotly_chart(
                    MACD(
                        data1,
                        num_period
                    ),
                    use_container_width=True
                )

        # ============== LINE CHART ==================
        elif chart_type == 'Line':

            if indicators == "RSI":
                st.plotly_chart(
                    close_chart(
                        data1,
                        num_period
                    ),
                    use_container_width=True
                )

                st.plotly_chart(
                    RSI(
                        data1,
                        num_period
                    ),
                    use_container_width=True
                )

            elif indicators == "Moving Average":
                st.plotly_chart(
                    moving_average(
                        data1,
                        num_period
                    ),
                    use_container_width=True
                )

            elif indicators == "MACD":
                st.plotly_chart(
                    MACD(
                        data1,
                        num_period
                    ),
                    use_container_width=True
                )

except Exception as e:
    st.error(f"Error loading stock data: {e}")
