"""Node: Generate synthetic sales data."""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sales.state import SalesState
from sales import config


def generate_sales_data(state: SalesState) -> SalesState:
    """
    Generate 180 days of synthetic daily sales data with:
    - Linear trend
    - Weekly seasonality (7-day cycle)
    - Monthly effects
    - Random noise
    
    Deterministic and reproducible with fixed random seed.
    """
    np.random.seed(config.RANDOM_SEED)
    
    # Time range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=config.HISTORICAL_DAYS - 1)
    date_range = pd.date_range(start=start_date, periods=config.HISTORICAL_DAYS, freq='D')
    
    # Base components
    n = config.HISTORICAL_DAYS
    t = np.arange(n)
    
    # 1. Linear trend: base 100 + 0.5 per day
    trend = 100 + 0.5 * t
    
    # 2. Weekly seasonality: 7-day cycle, amplitude 15
    weekly = 15 * np.sin(2 * np.pi * t / 7)
    
    # 3. Monthly effect: 30-day cycle, amplitude 10
    monthly = 10 * np.sin(2 * np.pi * t / 30)
    
    # 4. Random noise: standard normal, scale 5
    noise = np.random.normal(0, 5, n)
    
    # Combine all components
    sales = trend + weekly + monthly + noise
    
    # Ensure non-negative sales
    sales = np.maximum(sales, 1)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'sales': sales
    })
    
    df['date'] = pd.to_datetime(df['date'])
    
    state.raw_data = df
    return state
