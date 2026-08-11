import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA 
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

# GET STOCK DATA -
def get_data(ticker):
    stock_data = yf.download(ticker, start = "2024-01-01", auto_adjust=False)
    # return stock_data[['Close']]

    # Handle latest yfinance MultiIndex format
    if isinstance(stock_data.columns, pd.MultiIndex):
        close_price = stock_data["Close"].iloc[:, 0]
    else:
        close_price = stock_data["Close"]

    close_price = pd.Series(close_price).dropna()

    return close_price

# STATIONARITY CHECK -
def stationary_check(close_price):
    close_price = pd.Series(close_price).dropna()
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)
    return p_value

# ROLLING MEAN -
def get_rolling_mean(close_price):
    close_price = pd.Series(close_price)
    rolling_price = close_price.rolling(window = 7).mean().dropna()
    return rolling_price

# FIND DIFFERENCING ORDER -
def get_differencing_order(close_price):
    close_price = pd.Series(close_price).dropna()
    p_value = stationary_check(close_price)
    d = 0
    # Maximum differencing order = 2
    while p_value > 0.05 and d < 2:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)
    return d

# FIT ARIMA MODEL -
def fit_model(data, differencing_order):
    data = pd.Series(data).dropna()
    model = ARIMA(
        data, order = (
            30, differencing_order,
            30
        )
    )
    
    model_fit = model.fit()

    forecast_steps = 30
    forecast = model_fit.get_forecast(
        steps = forecast_steps
    )

    predictions = forecast.predicted_mean
    
    # Convert prediction to NumPy array
    predictions = np.asarray(predictions).flatten()
    
    return predictions

# EVALUATE MODEL -
def evaluate_model(original_price, differencing_order):
    original_price = pd.Series(original_price.flatten()).dropna()
    
    # Last 30 observations = test data
    train_data = original_price[:-30]
    test_data = original_price[-30:]
    
    # Forecast 30 values
    predictions = fit_model(
        train_data, 
        differencing_order
    )
    
    # Make sure both arrays have same length
    predictions = np.asarray(predictions).flatten()
    test_data = np.asarray(test_data).flatten()

    min_length = min(
        len(test_data),
        len(predictions)
    )

    test_data = test_data[:min_length]
    predictions = predictions[:min_length]
    
    rmse = np.sqrt(
        mean_squared_error(
            test_data, 
            predictions
        )
    )
    
    return round(float(rmse), 2)

# SCALING -
def scaling(close_price):
    scaler = StandardScaler()
    close_price = np.asarray(close_price).reshape(-1, 1)
    scaled_data = scaler.fit_transform(close_price)
    return scaled_data, scaler

# FORECAST FUTURE PRICES -
def get_forecast(original_price, differencing_order):
    original_price = pd.Series(original_price.squeeze()).dropna()
    
    predictions = fit_model(
        original_price, 
        differencing_order
    )
    
    # Start from Tomorrow
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days = 29)).strftime('%Y-%m-%d')
    
    forecast_index = pd.date_range(
        start = start_date, 
        end = end_date, 
        freq = 'D'
    )
    
    # Make sure lengths match
    forecast_index = forecast_index[:len(predictions)]
    forecast_df = pd.DataFrame(
        {
            "Close": predictions[:len(forecast_index)]
        },
        index = forecast_index,
    )
    
    return forecast_df

# INVERSE SCALING -
def inverse_scaling(scaler, scaled_data):
    scaled_data = np.asarray(scaled_data).reshape(-1, 1)
    
    close_price = scaler.inverse_transform(
        scaled_data
    )
    
    return close_price