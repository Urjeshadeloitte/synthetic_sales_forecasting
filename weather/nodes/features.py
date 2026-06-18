"""Feature engineering node: temporal and rolling average features."""

import numpy as np
import pandas as pd
from datetime import datetime

from weather.config import START_DATE, MA_7_DAYS, MA_30_DAYS
from weather.state import PipelineState


def engineer_features(state: PipelineState) -> dict:
    """
    Engineer seasonal and rolling average features.
    - Creates DataFrame from cleaned weather
    - Adds target variable (temp_mean = temp)
    - Adds temporal features: day_of_year, sin/cos seasonality
    - Adds rolling averages for 7 and 30 day windows
    - Drops rows with NaN from rolling calculations
    
    Returns:
        dict with key "features_df" containing processed DataFrame.
    """
    cleaned_weather = state.get("cleaned_weather", [])
    
    # Create DataFrame
    df = pd.DataFrame(cleaned_weather)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    
    # Target: mean temperature (in this case, just use the daily temp)
    df["temp_mean"] = df["temp"]
    
    # Temporal features
    df["day_of_year"] = df.index.dayofyear
    
    # Sin/cos encoding of day of year for seasonal patterns
    df["sin_doy"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
    df["cos_doy"] = np.cos(2 * np.pi * df["day_of_year"] / 365)
    
    # Rolling average features (on training portion only for now, we'll filter later)
    df["temp_ma_7d"] = df["temp"].rolling(window=MA_7_DAYS, min_periods=1).mean()
    df["temp_ma_30d"] = df["temp"].rolling(window=MA_30_DAYS, min_periods=1).mean()
    df["precip_ma_7d"] = df["precip"].rolling(window=MA_7_DAYS, min_periods=1).mean()
    df["humidity_ma_7d"] = df["humidity"].rolling(window=MA_7_DAYS, min_periods=1).mean()
    
    # Drop first 30 rows due to 30-day rolling average NaN values
    # (this ensures proper initialization of rolling features)
    df = df.iloc[MA_30_DAYS:].reset_index()
    
    return {"features_df": df}
