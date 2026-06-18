"""Configuration and constants for the weather forecasting pipeline."""

from datetime import datetime
from pathlib import Path

# Random seed for reproducibility
RANDOM_SEED = 42

# Date range for synthetic data generation
START_DATE = datetime(2024, 1, 1)
N_HISTORICAL_DAYS = 180
N_FORECAST_DAYS = 30

# Train/test split: days 0-149 = training, 150-179 = test
TRAIN_TEST_SPLIT_DAY = 150

# Output directory
OUTPUT_DIR = Path(__file__).parent / "output"

# Weather data validation ranges (for clipping outliers)
WEATHER_RANGES = {
    "temp": {"min": -10, "max": 40},  # Celsius
    "humidity": {"min": 0, "max": 100},  # Percentage
    "precip": {"min": 0, "max": 100},  # mm
    "windspeed": {"min": 0, "max": 50},  # m/s
    "pressure": {"min": 950, "max": 1050},  # hPa
}

# Feature engineering windows
MA_7_DAYS = 7
MA_30_DAYS = 30

# Model and output settings
MODEL_TYPE = "LinearRegression"
PLOT_FILENAME = "forecast_plot.png"
