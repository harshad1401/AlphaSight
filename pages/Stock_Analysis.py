# Importing libraries -
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.plotly_figure import plotly_table

# Setting Page Config -
st.set_page_config(
    page_title = "Stock Analysis",
    page_icon = "page_with_curl",
    layout = "wide"
)

st.title("Stock Analysis")

# Getting Input from User -
col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.selectbox("Choose a Stock: ", ['TSLA', 'AAPL', 'NFLX', 'MGM', 'AMZN', 'NVDA', 'GOOGL', 'META', 'MSFT', 'LLY', 'AMD', 'V', 'XOM', 'JNJ', 'MU', 'CSCO', 'BAC', 'INTC', 'ORCL', 'DELL', 'GS', 'JCI'])
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year -1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("Sector : ", stock.info['sector'])
st.write("Full-Time Employees : ", stock.info['fullTimeEmployees'])
st.write("Website : ", stock.info['website'])

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index = ['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [stock.info["marketCap"], stock.info["beta"], stock.info["trailingEps"], stock.info["trailingPE"]]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width = True)
with col2:
    df = pd.DataFrame(index = ['Quick Ratio', 'Revenue per Share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df[''] = [
        stock.info.get('quickRatio', 0),
        stock.info.get('revenuePerShare', 0),
        stock.info.get('profitMargins', 0),
        stock.info.get('debtToEquity', 0),
        stock.info.get('returnOnEquity', 0)
    ]
    
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width = True)

try:
    data = yf.download(ticker, start = start_date, end = end_date)

    col1, col2, col3 = st.columns(3)
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    col1.metric("Daily Change", f"{data['Close'].iloc[-1]:.2f}", f"{daily_change:.2f}")

    last_10_df = data.tail(10).sort_index(ascending = False).round(3)
    fig_df = plotly_table(last_10_df)

    st.write("##### Historical Data (Last 10 Days)")
    st.plotly_chart(fig_df, use_container_width = True)

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    num_period = ''
    with col1:
        if st.button["5D"]:
            num_period = '5D'
    with col2:
        if st.button["1M"]:
            num_period = '1M'
    with col3:
        if st.button["6M"]:
            num_period = '6M'
    with col4:
        if st.button["YTD"]:
            num_period = 'YTD'
    with col5:
        if st.button["1Y"]:
            num_period = '1Y'
    with col6:
        if st.button["5Y"]:
            num_period = '5Y'
    with col7:
        if st.button["MAX"]:
            num_period = 'MAX'

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        chart_type = st.selectbox('', ('Candle', 'Line'))
    with col2:
        if chart_type == 'Candle':
            indicators = st.selectbox('', ('RSI', 'MACD'))
        else:
            indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

    ticker_ = yf.Ticker(ticker)
    new_df1 = ticker_.history(period = 'max')
    data1 = ticker_.history(period = 'max')
    if num_period == '':

        if chart_type == 'Candle' and indicators == 'RSI':
            st.plotly_chart(candlestick(data1, '1y'), use_container_width = True)
            st.plotly_chart(RSI(data1, '1y'), use_container_width = True)

        if chart_type == 'Candle' and indicators == 'MACD':
            st.plotly_chart(candlestick(data1, '1y'), use_container_width = True)
            st.plotly_chart(MACD(data1, '1y'), use_container_width = True)

        if chart_type == 'Line' and indicators == 'RSI':
            st.plotly_chart(close_chart(data1, '1y'), use_container_width = True)
            st.plotly_chart(RSI(data1, '1y'), use_container_width = True)

        if chart_type == 'Line' and indicators == 'Moving Average':
            st.plotly_chart(moving_average(data1, '1y'), use_container_width = True)

        if chart_type == 'Line' and indicators == 'MACD':
            st.plotly_chart(close_chart(data1, '1y'), use_container_width = True)
            st.plotly_chart(MACD(data1, '1y'), use_container_width = True)

    else:

        if chart_type == 'Candle' and indicators == 'RSI':
            st.plotly_chart(candlestick(data1, num_period), use_container_width = True)
            st.plotly_chart(RSI(new_df1, num_period), use_container_width = True)

        if chart_type == 'Candle' and indicators == 'MACD':
            st.plotly_chart(candlestick(data1, num_period), use_container_width = True)
            st.plotly_chart(MACD(new_df1, num_period), use_container_width = True)

        if chart_type == 'Line' and indicators == 'RSI':
            st.plotly_chart(close_chart(data1, num_period), use_container_width = True)
            st.plotly_chart(RSI(new_df1, num_period), use_container_width = True)
        
        if chart_type == 'Line' and indicators == 'Moving Average':
            st.plotly_chart(moving_average(new_df1, num_period), use_container_width = True)

        if chart_type == 'Line' and indicators == 'MACD':
            st.plotly_chart(close_chart(data1, num_period), use_container_width = True)
            st.plotly_chart(MACD(new_df1, num_period), use_container_width = True)
except:
    st.write("")
