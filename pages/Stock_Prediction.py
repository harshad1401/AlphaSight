# Importing libraries -
import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

# CUSTOM CSS -
st.markdown("""
<style>

.stApp {
    background-color: #131722;
    color: white;
}

</style>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

# Import Dataset -
sp500 = pd.read_csv("sp500_companies.csv")

# Display Companies -
# st.dataframe(sp500)

# Get ticker list -
tickers_list = sp500['Symbol'].to_list()

with col1:
    ticker = st.selectbox("Choose a Stock: ", tickers_list)

rmse = 0

st.subheader("Predicting Next 30 Days Close Price for: " + ticker)

try:

    # Get Stock Data -
    close_price = get_data(ticker)

    # Calculating Rolling Mean -
    rolling_price = get_rolling_mean(close_price)

    # Find Differencing Order -
    differencing_order = get_differencing_order(
        rolling_price
    )

    # Scale Data -
    scaled_data, scaler = scaling(rolling_price)

    # Evaluate ARIMA Model -
    rmse = evaluate_model(
        scaled_data,
        differencing_order
    )

    st.write("Model RMSE Score: ", round(float(rmse), 4))

    # Forecast -
    forecast = get_forecast(scaled_data, differencing_order)

    # Inverse Scaling -
    forecast['Close'] = inverse_scaling(
        scaler,
        forecast['Close']
    )

    st.write("##### Forecast Data (Next 30 Days)")

    # Forecast Table -
    fig_tail = plotly_table(
        forecast.sort_index(
            ascending=True
        )
        .round(3)
    )

    fig_tail.update_layout(height=220)
    st.plotly_chart(fig_tail, use_container_width=True)

    # STOCK PRICE FORECAST CHART -

    st.markdown("### 📈 Stock Price Forecast Chart")

    # Combine historical data and forecast data
    combined_data = pd.concat(
        [rolling_price, forecast],
        axis=0
    )

    # Remove missing values
    combined_data = combined_data.dropna(subset=["Close"])

    # Sort by date
    combined_data = combined_data.sort_index()

    # Create Plotly figure
    fig = go.Figure()

    # Add Close Price
    fig.add_trace(
        go.Scatter(
            x=combined_data.index,
            y=combined_data["Close"],
            mode="lines",
            name="Close Price",
            line=dict(width=2, color='green')
        )
    )

    # Chart layout
    fig.update_layout(
        title=f"{ticker} - Stock Price Forecast",
        xaxis_title="Date",
        yaxis_title="Close Price",
        height=600,
        hovermode="x unified",
        template="plotly_white",
    )

    # Display chart
    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Error while predicting {ticker}: {e}")
