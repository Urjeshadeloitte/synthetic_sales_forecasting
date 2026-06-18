"""Node: Engineer time-based and seasonal features."""
import pandas as pd
import numpy as np
from sales.state import SalesState
from sales import config


def engineer_features(state: SalesState) -> SalesState:
    """
    Engineer time-based and seasonal features:
    - Day of week (0-6)
    - Day of month (1-31)
    - Day of year (1-365/366)
    - Week of year (1-52/53)
    - Is weekend flag
    - Lagged features (previous day, 7 days, 30 days)
    - Rolling averages (7-day and 30-day)
    """
    df = state.cleaned_data.copy()
    
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Time-based features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Lagged features
    df['sales_lag_1'] = df['sales'].shift(1)
    df['sales_lag_7'] = df['sales'].shift(7)
    df['sales_lag_30'] = df['sales'].shift(30)
    
    # Rolling averages
    df['sales_rolling_7'] = df['sales'].rolling(window=7, min_periods=1).mean()
    df['sales_rolling_30'] = df['sales'].rolling(window=30, min_periods=1).mean()
    
    # Trigonometric features for seasonality
    df['day_of_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['day_of_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    # Fill remaining NaN values with forward/backward fill
    df = df.ffill().bfill()
    
    state.features_data = df
    state.metrics['features_count'] = len(df.columns) - 2  # Exclude date and sales
    
    return state
