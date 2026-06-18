"""Plotting utilities for sales forecast visualization."""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_forecast(historical: pd.DataFrame, forecast: pd.DataFrame, output_path: str) -> None:
    """
    Create and save a plot showing historical sales and 30-day forecast.
    
    Parameters:
    -----------
    historical : pd.DataFrame
        Historical sales data with 'date' and 'sales' columns
    forecast : pd.DataFrame
        Forecast data with 'date' and 'sales' columns
    output_path : str
        Path to save the PNG file
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot historical data
    ax.plot(historical['date'], historical['sales'], 
            label='Historical Sales', color='blue', linewidth=2, marker='o', markersize=3)
    
    # Plot forecast
    ax.plot(forecast['date'], forecast['sales'], 
            label='30-Day Forecast', color='red', linewidth=2, marker='s', markersize=3, linestyle='--')
    
    # Add vertical line at forecast start
    forecast_start = forecast['date'].iloc[0]
    ax.axvline(x=forecast_start, color='gray', linestyle=':', alpha=0.7, linewidth=1.5)
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Sales', fontsize=12, fontweight='bold')
    ax.set_title('Sales Forecasting: 180-Day History + 30-Day Forecast', 
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate(rotation=45, ha='right')
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()
