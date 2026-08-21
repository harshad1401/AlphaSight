# Importing libraries -
import plotly.express as px
import numpy as np

# Function to Plot interactive plotly chart -
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)
    fig.update_layout(width = 450, margin = dict(l = 20, r = 20, t = 50, b = 20), legend = dict(orientation = 'h', yanchor = "bottom", y = 1.02, xanchor = 'right', x = 1))
    
    return fig

# Function to Normalize the prices based on the initial price -
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = (df[i]/df[i].iloc[0]) * 100

    return df

# Function to Calculate Daily Returns -
def daily_returns(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        df_daily_return[i] = df[i].pct_change()
            
    df_daily_return = df_daily_return.dropna()
    
    return df_daily_return

# Function to Calculate Beta -
def calculate_beta(stocks_daily_return, stock):

    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock], 1)

    return b, a
