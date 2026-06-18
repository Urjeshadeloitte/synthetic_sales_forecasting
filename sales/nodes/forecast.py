"""Node: Forecast next 30 days of sales."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sales.state import SalesState
from sales import config


def forecast_sales(state: SalesState) -> SalesState:
    """
    Forecast the next 30 days of sales using the trained model.
    
    Iteratively generates features for future days and makes predictions.
    """
    np.random.seed(config.RANDOM_SEED)
    
    df = state.features_data.copy()
    model = state.model
    
    # Feature column names
    feature_cols = state.metrics['feature_names']
    
    # Starting point for forecast
    last_date = df['date'].iloc[-1]
    last_sales = df['sales'].iloc[-1]
    last_sales_lag_1 = df['sales'].iloc[-1]
    last_sales_lag_7 = df['sales'].iloc[-7]
    last_sales_lag_30 = df['sales'].iloc[-30]
    last_sales_rolling_7 = df['sales'].iloc[-7:].mean()
    last_sales_rolling_30 = df['sales'].iloc[-30:].mean()
    
    forecast_records = []
    
    for i in range(1, config.FORECAST_DAYS + 1):
        forecast_date = last_date + timedelta(days=i)
        
        # Compute time-based features
        day_of_week = forecast_date.dayofweek
        day_of_month = forecast_date.day
        day_of_year = forecast_date.timetuple().tm_yday
        week_of_year = forecast_date.isocalendar()[1]
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Trigonometric seasonality features
        day_of_week_sin = np.sin(2 * np.pi * day_of_week / 7)
        day_of_week_cos = np.cos(2 * np.pi * day_of_week / 7)
        day_of_year_sin = np.sin(2 * np.pi * day_of_year / 365)
        day_of_year_cos = np.cos(2 * np.pi * day_of_year / 365)
        
        # Use previous predicted value for lags
        prev_sales = forecast_records[-1]['sales'] if forecast_records else last_sales
        
        # Rolling averages (update as we forecast)
        if len(forecast_records) >= 7:
            sales_rolling_7 = np.mean([r['sales'] for r in forecast_records[-7:]])
        else:
            sales_rolling_7 = last_sales_rolling_7
        
        if len(forecast_records) >= 30:
            sales_rolling_30 = np.mean([r['sales'] for r in forecast_records[-30:]])
        else:
            sales_rolling_30 = last_sales_rolling_30
        
        # Lags (use historical if not enough forecasts yet)
        sales_lag_1 = prev_sales
        sales_lag_7 = forecast_records[-7]['sales'] if len(forecast_records) >= 7 else last_sales_lag_7
        sales_lag_30 = forecast_records[-30]['sales'] if len(forecast_records) >= 30 else last_sales_lag_30
        
        # Construct feature vector
        feature_dict = {
            'day_of_week': day_of_week,
            'day_of_month': day_of_month,
            'day_of_year': day_of_year,
            'week_of_year': week_of_year,
            'is_weekend': is_weekend,
            'sales_lag_1': sales_lag_1,
            'sales_lag_7': sales_lag_7,
            'sales_lag_30': sales_lag_30,
            'sales_rolling_7': sales_rolling_7,
            'sales_rolling_30': sales_rolling_30,
            'day_of_week_sin': day_of_week_sin,
            'day_of_week_cos': day_of_week_cos,
            'day_of_year_sin': day_of_year_sin,
            'day_of_year_cos': day_of_year_cos,
        }
        
        # Reorder features to match model training
        X_forecast = np.array([feature_dict[col] for col in feature_cols]).reshape(1, -1)
        
        # Predict
        predicted_sales = model.predict(X_forecast)[0]
        predicted_sales = max(predicted_sales, 1)  # Ensure positive
        
        forecast_records.append({
            'date': forecast_date,
            'sales': predicted_sales
        })
    
    forecast_df = pd.DataFrame(forecast_records)
    forecast_df['date'] = pd.to_datetime(forecast_df['date'])
    
    state.forecast = forecast_df
    state.metrics['forecast_records'] = len(forecast_df)
    
    return state
