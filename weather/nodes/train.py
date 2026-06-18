"""Model training node: split data and train LinearRegression."""

import numpy as np
from sklearn.linear_model import LinearRegression

from weather.config import RANDOM_SEED, TRAIN_TEST_SPLIT_DAY, MA_30_DAYS
from weather.state import PipelineState


def train_model(state: PipelineState) -> dict:
    """
    Split features into train/test and train a LinearRegression model.
    - Train: days 0 to 149 (150 samples)
    - Test: days 150 to 179 (30 samples)
    - Features: day_of_year, sin/cos, humidity, precip, windspeed, pressure, rolling averages
    - Target: temp_mean
    
    Returns:
        dict with "model" (trained LinearRegression) and "train_test_split" (both DataFrames).
    """
    features_df = state.get("features_df").copy()
    
    # Adjust split day accounting for dropped rows (first 30 days removed)
    # Original day 150 becomes index 120 (150 - 30)
    split_idx = TRAIN_TEST_SPLIT_DAY - MA_30_DAYS
    
    train_df = features_df.iloc[:split_idx]
    test_df = features_df.iloc[split_idx:]
    
    # Feature columns
    feature_cols = [
        "day_of_year", "sin_doy", "cos_doy",
        "humidity", "precip", "windspeed", "pressure",
        "temp_ma_7d", "temp_ma_30d", "precip_ma_7d", "humidity_ma_7d"
    ]
    
    X_train = train_df[feature_cols]
    y_train = train_df["temp_mean"]
    
    X_test = test_df[feature_cols]
    y_test = test_df["temp_mean"]
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return {
        "model": model,
        "train_test_split": {
            "train": train_df,
            "test": test_df,
        }
    }
