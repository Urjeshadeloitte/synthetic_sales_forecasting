"""State definition for the sales forecasting pipeline."""
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import numpy as np


@dataclass
class SalesState:
    """State container for the sales forecasting pipeline."""
    
    # Raw data
    raw_data: Optional[pd.DataFrame] = None
    
    # Cleaned data
    cleaned_data: Optional[pd.DataFrame] = None
    
    # Engineered features
    features_data: Optional[pd.DataFrame] = None
    
    # Model and forecast
    model: Optional[object] = None
    forecast: Optional[pd.DataFrame] = None
    
    # Metrics
    metrics: dict = field(default_factory=dict)
