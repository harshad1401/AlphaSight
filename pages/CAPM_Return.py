# Importing libraries -
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import CAPM_Functions

st.set_page_config(
    page_title="Capital Asset Pricing Model",
    page_icon="chart_with_upwards_trend",
    layout='wide'
)

st.title("Capital Asset Pricing Model")

# Getting Input from User -
col1, col2 = st.columns([1, 1])

# Import Dataset -
sp500 = pd.read_csv("sp500_companies.csv")

# Display Companies -
# st.dataframe(sp500)

# Get ticker list -
tickers_list = sp500['Symbol'].to_list()

with col1:
    stocks_list = st.multiselect("Choose 4 Stocks", tickers_list, {'TSLA', 'AAPL', 'AMZN', 'GOOGL'})
with col2:
    year = st.number_input("Number of years: ", 1, 10)

# Downloading Data for SP500 -
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year-year,
                          datetime.date.today().month, datetime.date.today().day)
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
    # print(SP500.head)

    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[f'{stock}'] = data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']
    # print(stocks_df.dtypes)
    # print(SP500.dtypes)

    stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
    # print(stocks_df)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Price of all the Stocks')
        st.plotly_chart(CAPM_Functions.interactive_plot(stocks_df))
    with col2:
        st.markdown('### Price of all the Stocks (After Normalizing)')
        st.plotly_chart(CAPM_Functions.interactive_plot(
            CAPM_Functions.normalize(stocks_df)))

    stocks_daily_return = CAPM_Functions.daily_returns(stocks_df)
    # print(stocks_daily_return.head)

    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'sp500':
            b, a = CAPM_Functions.calculate_beta(stocks_daily_return, i)

            beta[i] = b
            alpha[i] = a
    print(beta, alpha)

    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    # CALCULATED RETURN USING CAPM -

    st.markdown("### 💰 Calculated Return using CAPM")

    # Risk-free rate -
    # Get latest 10-Year US Treasury Yield
    treasury = web.DataReader(
        "DGS10",
        "fred",
        start,
        end
    )

    rf_percent = treasury["DGS10"].dropna().iloc[-1]

    # Convert percentage to decimal
    rf = rf_percent / 100

    # S&P 500 Daily Returns -
    sp500_returns = stocks_daily_return["sp500"].dropna()

    # Annualized Market Return -
    sp500_returns = stocks_daily_return["sp500"].replace(
        [float("inf"), float("-inf")],
        pd.NA
    ).dropna()
    
    rm = (1 + sp500_returns).prod() ** (
        252 / len(sp500_returns)
    ) - 1

    # CAPM Inputs -
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Risk-Free Rate",
            f"{rf * 100:.2f}%"
        )

    with col2:
        st.metric(
            "Market Return",
            f"{rm * 100:.2f}%"
        )

    with col3:
        st.metric(
            "Selected Stocks",
            len(stocks_list)
        )

    # Calculate Expected Return -
    return_values = []

    for stock in stocks_list:

        # Get beta for current stock -
        stock_beta = float(beta[stock])

        # CAPM Formula -
        capm_return = rf + stock_beta * (rm - rf)

        # Convert decimal to percentage -
        capm_return_percentage = capm_return * 100

        return_values.append(
            round(capm_return_percentage, 2)
        )

    # Create Result DataFrame -

    return_df = pd.DataFrame({

        "Stock": stocks_list,

        "Beta": [
            round(float(beta[stock]), 2)
            for stock in stocks_list
        ],

        "Expected Return (%)": return_values
    })

    # Display Results -

    st.dataframe(
        return_df,
        use_container_width=True,
        hide_index=True
    )
except:
    st.write("")
