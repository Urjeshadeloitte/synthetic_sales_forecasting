"""Data cleaning and validation node."""

import numpy as np

from weather.config import WEATHER_RANGES
from weather.state import PipelineState


def clean_weather(state: PipelineState) -> dict:
    """
    Validate and clean raw weather data.
    - Clips values to valid ranges
    - Fills NaN with forward-fill then backward-fill
    
    Returns:
        dict with key "cleaned_weather" containing validated list of dicts.
    """
    raw_weather = state.get("raw_weather", [])
    cleaned_weather = []
    
    for record in raw_weather:
        cleaned_record = record.copy()
        
        # Clip each field to valid range
        for field, limits in WEATHER_RANGES.items():
            if field in cleaned_record:
                value = cleaned_record[field]
                if not np.isnan(value):
                    cleaned_record[field] = np.clip(
                        value, limits["min"], limits["max"]
                    )
        
        cleaned_weather.append(cleaned_record)
    
    # Fill any remaining NaN (forward-fill then backward-fill)
    values_by_field = {field: [] for field in WEATHER_RANGES.keys()}
    
    for record in cleaned_weather:
        for field in WEATHER_RANGES.keys():
            val = record.get(field, np.nan)
            if np.isnan(val):
                # Forward-fill: use last known value
                if values_by_field[field]:
                    val = values_by_field[field][-1]
            if not np.isnan(val):
                values_by_field[field].append(val)
    
    # Backward-fill for any remaining NaN at start
    for i, record in enumerate(cleaned_weather):
        for field in WEATHER_RANGES.keys():
            if np.isnan(record.get(field, np.nan)):
                # Find first non-NaN value
                for j in range(i + 1, len(cleaned_weather)):
                    if not np.isnan(cleaned_weather[j].get(field, np.nan)):
                        record[field] = cleaned_weather[j][field]
                        break
    
    return {"cleaned_weather": cleaned_weather}
