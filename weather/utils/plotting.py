"""Plotting utilities for forecast visualization."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_forecast(
    historical_df: pd.DataFrame,
    test_df: pd.DataFrame,
    test_preds: np.ndarray,
    forecast_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Create a 3-part forecast visualization:
    1. Historical data (days 0-180): blue line
    2. Test set (days 150-179): actual (green) vs predicted (red)
    3. 30-day forecast (days 180-210): orange line
    
    Args:
        historical_df: DataFrame with historical weather and features
        test_df: DataFrame with test set data
        test_preds: Array of test predictions
        forecast_df: DataFrame with 30-day forecast
        output_path: Path to save PNG file
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # X-axis: continuous day indices
    hist_days = np.arange(len(historical_df))
    test_days = np.arange(len(historical_df), len(historical_df) + len(test_df))
    forecast_days = np.arange(
        len(historical_df) + len(test_df),
        len(historical_df) + len(test_df) + len(forecast_df)
    )
    
    # Plot 1: Historical temperature (blue)
    ax.plot(
        hist_days, historical_df["temp_mean"], 
        color="blue", linewidth=2, label="Historical Actual", zorder=2
    )
    
    # Plot 2: Test actual vs predicted
    ax.plot(
        test_days, test_df["temp_mean"].values,
        color="green", linewidth=2, marker="o", markersize=5,
        label="Test Actual", zorder=2
    )
    ax.plot(
        test_days, test_preds,
        color="red", linewidth=2, marker="x", markersize=5,
        label="Test Predicted", linestyle="--", zorder=2
    )
    
    # Plot 3: 30-day forecast (orange)
    ax.plot(
        forecast_days, forecast_df["predicted_temp"],
        color="orange", linewidth=2, marker="s", markersize=5,
        label="30-Day Forecast", zorder=2
    )
    
    # Styling
    ax.set_xlabel("Day Index", fontsize=12)
    ax.set_ylabel("Temperature (°C)", fontsize=12)
    ax.set_title("Weather Forecast: Historical Data, Test Period, and 30-Day Forecast", fontsize=14)
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Add vertical separators
    ax.axvline(x=len(historical_df) - 0.5, color="gray", linestyle=":", alpha=0.5)
    ax.axvline(x=len(historical_df) + len(test_df) - 0.5, color="gray", linestyle=":", alpha=0.5)
    
    # Save figure
    fig.tight_layout()
    fig.savefig(output_path, dpi=100)
    plt.close(fig)
