# Importing libraries -
import yfinance as yf
import pandas as pd
import streamlit as st
import yfinance as yf
import pandas_datareader.data as web
import datetime
import CAPM_Functions

st.set_page_config(
    page_title = "Beta", 
    page_icon = "chart_with_upwards_trend", 
    layout = 'wide'
)

st.title("Calculate Beta and Return for Individual Stock")

# Getting Input from User -
col1, col2 = st.columns([1, 1])
with col1:
    stock = st.selectbox("Choose a Stocks", ['TSLA', 'AAPL', 'NFLX', 'MGM', 'AMZN', 'NVDA', 'GOOGL'])
with col2:
    year = st.number_input("Number of years: ", 1, 10)
    
# Downloading Data for SP500 -
end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
SP500 = web.DataReader(['sp500'], 'fred', start, end)

stocks_df = pd.DataFrame()

data = yf.download(stock, period = f'{year}y')
stocks_df[f'{stock}'] = data['Close']

stocks_df.reset_index(inplace = True)
SP500.reset_index(inplace = True)
SP500.columns = ['Date', 'sp500']

stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df = pd.merge(stocks_df, SP500, on = 'Date', how = 'inner')
print(stocks_df)
    
# Calculate Daily Returns -
stocks_df['Return'] = stocks_df[stock].pct_change()
SP500['Return'] = SP500['sp500'].pct_change()

# Merge Returns -
df = pd.concat([stocks_df['Return'], SP500['Return']], axis=1)
df.columns = ['Stock_Return', 'Market_Return']

# Remove Missing Values -
df.dropna(inplace=True)

# Calculate Covariance -
covariance = df['Stock_Return'].cov(df['Market_Return'])

# Calculate Market Variance
market_variance = df['Market_Return'].var()

# Calculate Beta -
beta = covariance / market_variance

# print("Stock Beta =", round(beta, 4))
# beta = covariance / market_variance

st.write("### Beta : ", round(beta, 4))

# EXPECTED RETURN USING CAPM -

# Risk-Free Rate
rf = 0.00

# Annualized Market Return
rm = df["Market_Return"].mean() * 252

# CAPM Formula
expected_return = rf + beta * (rm - rf)

# Convert decimal to percentage
expected_return_percentage = expected_return * 100

# Display Expected Return
st.write("### Expected Return: ", f"{expected_return_percentage:.2f}%")