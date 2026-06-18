"""Configuration for the sales forecasting pipeline."""

# Random seed for reproducibility
RANDOM_SEED = 42

# Data generation parameters
HISTORICAL_DAYS = 180
FORECAST_DAYS = 30

# Output paths
OUTPUT_DIR = "sales/output"
CSV_RAW = "sales/output/raw_sales.csv"
CSV_CLEANED = "sales/output/cleaned_sales.csv"
CSV_FEATURES = "sales/output/features_engineered.csv"
CSV_FORECAST = "sales/output/forecast_30d.csv"
PNG_FORECAST = "sales/output/forecast_plot.png"

# Feature engineering parameters
SEASONAL_PERIODS = 7  # Weekly seasonality
MONTHLY_PERIODS = 30  # Monthly effect

# Model parameters
TEST_SIZE = 0.2  # For evaluation metrics
