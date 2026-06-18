"""Metrics calculation node: RMSE, MAE, R²."""

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from weather.state import PipelineState


def calculate_metrics(state: PipelineState) -> dict:
    """
    Calculate evaluation metrics on the test set.
    - RMSE: Root Mean Squared Error
    - MAE: Mean Absolute Error
    - R²: Coefficient of determination
    
    Returns:
        dict with key "metrics" containing metric values.
    """
    model = state.get("model")
    train_test_split = state.get("train_test_split", {})
    
    if model is None or not train_test_split:
        raise ValueError("Model or train_test_split not found in state")
    
    test_df = train_test_split.get("test")
    if test_df is None:
        raise ValueError("Test data not found")
    
    # Feature columns (must match training)
    feature_cols = [
        "day_of_year", "sin_doy", "cos_doy",
        "humidity", "precip", "windspeed", "pressure",
        "temp_ma_7d", "temp_ma_30d", "precip_ma_7d", "humidity_ma_7d"
    ]
    
    X_test = test_df[feature_cols]
    y_test = test_df["temp_mean"]
    
    # Generate predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Forecast stats
    mean_pred = np.mean(y_pred)
    std_pred = np.std(y_pred)
    min_pred = np.min(y_pred)
    max_pred = np.max(y_pred)
    
    metrics = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "mean_pred": mean_pred,
        "std_pred": std_pred,
        "min_pred": min_pred,
        "max_pred": max_pred,
    }
    
    return {"metrics": metrics}
