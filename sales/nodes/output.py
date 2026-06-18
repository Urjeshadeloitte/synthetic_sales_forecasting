"""Node: Write outputs (CSV, PNG, metrics)."""
import os
import pandas as pd
from sales.state import SalesState
from sales import config
from sales.utils.plotting import plot_forecast
from sales.utils.reporting import print_metrics


def write_outputs(state: SalesState) -> SalesState:
    """
    Write all outputs:
    - raw_sales.csv: Raw generated data
    - cleaned_sales.csv: Cleaned data
    - features_engineered.csv: Data with engineered features
    - forecast_30d.csv: 30-day forecast
    - forecast_plot.png: Visualization of historical + forecast
    - Print console metrics
    """
    # Ensure output directory exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Write raw data
    state.raw_data.to_csv(config.CSV_RAW, index=False)
    state.metrics['raw_csv'] = config.CSV_RAW
    
    # Write cleaned data
    state.cleaned_data.to_csv(config.CSV_CLEANED, index=False)
    state.metrics['cleaned_csv'] = config.CSV_CLEANED
    
    # Write features data (select main columns for clarity)
    feature_output = state.features_data[['date', 'sales', 'day_of_week', 'day_of_month', 
                                          'day_of_year', 'week_of_year', 'is_weekend',
                                          'sales_lag_1', 'sales_lag_7', 'sales_lag_30',
                                          'sales_rolling_7', 'sales_rolling_30']].copy()
    feature_output.to_csv(config.CSV_FEATURES, index=False)
    state.metrics['features_csv'] = config.CSV_FEATURES
    
    # Write forecast
    state.forecast.to_csv(config.CSV_FORECAST, index=False)
    state.metrics['forecast_csv'] = config.CSV_FORECAST
    
    # Generate and save plot
    plot_forecast(state.cleaned_data, state.forecast, config.PNG_FORECAST)
    state.metrics['forecast_plot'] = config.PNG_FORECAST
    
    # Print metrics to console
    print_metrics(state.metrics)
    
    return state
