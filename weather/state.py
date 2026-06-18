"""LangGraph pipeline state schema."""

from typing import TypedDict, Any, Optional
import pandas as pd
from sklearn.linear_model import LinearRegression


class PipelineState(TypedDict, total=False):
    """
    Shared state for the weather forecasting pipeline.
    All fields are optional to allow partial state initialization.
    """

    # Phase 1: Generated synthetic weather (180 days)
    raw_weather: list[dict[str, Any]]

    # Phase 2: Cleaned and validated weather
    cleaned_weather: list[dict[str, Any]]

    # Phase 3: Features with engineered seasonal/rolling components
    features_df: pd.DataFrame

    # Phase 4: Train/test split data
    train_test_split: dict[str, pd.DataFrame]

    # Phase 5: Trained model
    model: LinearRegression

    # Phase 6: 30-day forecast
    forecast_30d: pd.DataFrame

    # Phase 7: Evaluation metrics
    metrics: dict[str, float]

    # Control: Track outputs saved
    outputs_saved: bool
