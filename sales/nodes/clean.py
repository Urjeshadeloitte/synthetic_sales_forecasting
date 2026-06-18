"""Node: Clean and validate sales data."""
import pandas as pd
import numpy as np
from sales.state import SalesState


def clean_sales_data(state: SalesState) -> SalesState:
    """
    Clean and validate sales data:
    - Remove duplicates by date
    - Handle missing values
    - Remove outliers (beyond 3 standard deviations)
    - Ensure monotonic date ordering
    """
    df = state.raw_data.copy()
    
    # 1. Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # 2. Remove duplicate dates (keep first occurrence)
    df = df.drop_duplicates(subset=['date'], keep='first')
    
    # 3. Handle missing values via forward fill (if any)
    df['sales'] = df['sales'].ffill().bfill()
    
    # 4. Remove outliers beyond 3 standard deviations
    mean = df['sales'].mean()
    std = df['sales'].std()
    lower_bound = mean - 3 * std
    upper_bound = mean + 3 * std
    
    initial_count = len(df)
    df = df[(df['sales'] >= lower_bound) & (df['sales'] <= upper_bound)]
    outliers_removed = initial_count - len(df)
    
    # 5. Ensure positive sales
    df['sales'] = df['sales'].clip(lower=0.01)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    state.cleaned_data = df
    state.metrics['outliers_removed'] = outliers_removed
    state.metrics['final_record_count'] = len(df)
    
    return state
