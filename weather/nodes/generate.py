"""Data generation node: creates 180 days of synthetic weather."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from weather.config import RANDOM_SEED, START_DATE, N_HISTORICAL_DAYS
from weather.state import PipelineState


def generate_weather_data(state: PipelineState) -> dict:
    """
    Generate 180 days of deterministic synthetic weather data.
    Uses fixed random seed to ensure byte-identical results across runs.
    
    Returns:
        dict with key "raw_weather" containing list of daily weather dicts.
    """
    np.random.seed(RANDOM_SEED)
    
    raw_weather = []
    
    for day_offset in range(N_HISTORICAL_DAYS):
        current_date = START_DATE + timedelta(days=day_offset)
        day_of_year = current_date.timetuple().tm_yday
        
        # Seasonal temperature pattern: warmer in summer, colder in winter
        # Base temp varies with day of year (cosine pattern)
        base_temp = 15 + 10 * np.cos(2 * np.pi * (day_of_year - 80) / 365)
        temp = base_temp + np.random.normal(0, 2)  # Add noise
        
        # Humidity: inverse correlation with temperature
        humidity = 70 - 0.3 * temp + np.random.normal(0, 5)
        
        # Precipitation: random events, slightly more in warmer months
        precip_base = 5 if day_of_year > 150 else 3
        precip = max(0, precip_base + np.random.normal(0, 3))
        
        # Wind speed: moderate variation
        windspeed = 8 + np.random.normal(0, 2)
        
        # Pressure: slight daily variation
        pressure = 1013 + np.random.normal(0, 3)
        
        raw_weather.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "temp": temp,
            "humidity": humidity,
            "precip": precip,
            "windspeed": windspeed,
            "pressure": pressure,
        })
    
    return {"raw_weather": raw_weather}
