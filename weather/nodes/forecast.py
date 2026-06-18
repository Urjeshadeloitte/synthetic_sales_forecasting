"""Forecasting node: predict next 30 days."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from weather.config import START_DATE, N_HISTORICAL_DAYS, N_FORECAST_DAYS, MA_30_DAYS, RANDOM_SEED
from weather.state import PipelineState


def forecast_next_30_days(state: PipelineState) -> dict:
    """
    Generate forecast for the next 30 days using the trained model.
    Creates feature vectors for future days and predicts temperature.
    Uses fixed random seed offset for deterministic synthetic feature generation.
    
    Returns:
        dict with key "forecast_30d" containing DataFrame with predictions.
    """
    model = state.get("model")
    features_df = state.get("features_df")
    
    if model is None or features_df is None:
        raise ValueError("Model or features_df not found in state")
    
    # Get historical data for computing rolling averages
    hist_data = features_df.copy()
    
    forecast_records = []
    
    # Get last date from features_df
    last_row = features_df.iloc[-1]
    if isinstance(last_row["date"], str):
        last_date = datetime.strptime(last_row["date"], "%Y-%m-%d")
    else:
        # If it's already a datetime/Timestamp object
        last_date = pd.Timestamp(last_row["date"]).to_pydatetime()
    
    # Use last 30 days of historical data for rolling average computation
    last_30_temps = hist_data["temp"].tail(30).values
    last_30_precips = hist_data["precip"].tail(30).values
    last_30_humidities = hist_data["humidity"].tail(30).values
    
    for day_offset in range(1, N_FORECAST_DAYS + 1):
        # Set seed deterministically for this forecast day
        # Using RANDOM_SEED + 1000 + day_offset to avoid colliding with generation phase
        np.random.seed(RANDOM_SEED + 1000 + day_offset)
        
        forecast_date = last_date + timedelta(days=day_offset)
        day_of_year = forecast_date.timetuple().tm_yday
        
        # Generate synthetic features for future day
        # Using same generation logic as original synthetic data for consistency
        base_temp = 15 + 10 * np.cos(2 * np.pi * (day_of_year - 80) / 365)
        temp_synthetic = base_temp + np.random.normal(0, 2)
        
        humidity_synthetic = 70 - 0.3 * temp_synthetic + np.random.normal(0, 5)
        precip_synthetic = max(0, (5 if day_of_year > 150 else 3) + np.random.normal(0, 3))
        windspeed_synthetic = 8 + np.random.normal(0, 2)
        pressure_synthetic = 1013 + np.random.normal(0, 3)
        
        # Compute rolling averages from historical + forecast data so far
        all_temps = np.concatenate([last_30_temps, [rec["temp"] for rec in forecast_records] if forecast_records else []])
        all_precips = np.concatenate([last_30_precips, [rec["precip"] for rec in forecast_records] if forecast_records else []])
        all_humidities = np.concatenate([last_30_humidities, [rec["humidity"] for rec in forecast_records] if forecast_records else []])
        
        temp_ma_7d = np.mean(all_temps[-7:]) if len(all_temps) >= 7 else np.mean(all_temps)
        temp_ma_30d = np.mean(all_temps[-30:]) if len(all_temps) >= 30 else np.mean(all_temps)
        precip_ma_7d = np.mean(all_precips[-7:]) if len(all_precips) >= 7 else np.mean(all_precips)
        humidity_ma_7d = np.mean(all_humidities[-7:]) if len(all_humidities) >= 7 else np.mean(all_humidities)
        
        # Create feature vector
        features = np.array([[
            day_of_year,
            np.sin(2 * np.pi * day_of_year / 365),
            np.cos(2 * np.pi * day_of_year / 365),
            humidity_synthetic,
            precip_synthetic,
            windspeed_synthetic,
            pressure_synthetic,
            temp_ma_7d,
            temp_ma_30d,
            precip_ma_7d,
            humidity_ma_7d,
        ]])
        
        # Predict temperature
        predicted_temp = model.predict(features)[0]
        
        forecast_records.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "predicted_temp": predicted_temp,
            "day_of_year": day_of_year,
            "temp": temp_synthetic,  # Store synthetic features for rolling avg computation
            "precip": precip_synthetic,
            "humidity": humidity_synthetic,
        })
    
    forecast_df = pd.DataFrame(forecast_records)
    
    return {"forecast_30d": forecast_df}
