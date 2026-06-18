"""Output node: save CSVs and generate plot."""

import pandas as pd

from weather.config import OUTPUT_DIR
from weather.utils.plotting import plot_forecast
from weather.state import PipelineState


def save_outputs(state: PipelineState) -> dict:
    """
    Save all outputs to weather/output/ directory:
    - raw_weather.csv: Original 180 days of synthetic data
    - cleaned_weather.csv: Validated data
    - features_engineered.csv: Features with temporal and rolling components
    - forecast_30d.csv: 30-day predictions
    - forecast_plot.png: Visualization of historical + forecast
    
    Returns:
        dict with key "outputs_saved" set to True.
    """
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get state data
    raw_weather = state.get("raw_weather", [])
    cleaned_weather = state.get("cleaned_weather", [])
    features_df = state.get("features_df")
    forecast_30d = state.get("forecast_30d")
    train_test_split = state.get("train_test_split", {})
    
    # Save raw weather
    if raw_weather:
        raw_df = pd.DataFrame(raw_weather)
        raw_df.to_csv(OUTPUT_DIR / "raw_weather.csv", index=False)
    
    # Save cleaned weather
    if cleaned_weather:
        cleaned_df = pd.DataFrame(cleaned_weather)
        cleaned_df.to_csv(OUTPUT_DIR / "cleaned_weather.csv", index=False)
    
    # Save engineered features
    if features_df is not None:
        features_df.to_csv(OUTPUT_DIR / "features_engineered.csv", index=False)
    
    # Save forecast
    if forecast_30d is not None:
        forecast_30d.to_csv(OUTPUT_DIR / "forecast_30d.csv", index=False)
    
    # Generate plot
    test_df = train_test_split.get("test")
    if features_df is not None and forecast_30d is not None and test_df is not None:
        model = state.get("model")
        feature_cols = [
            "day_of_year", "sin_doy", "cos_doy",
            "humidity", "precip", "windspeed", "pressure",
            "temp_ma_7d", "temp_ma_30d", "precip_ma_7d", "humidity_ma_7d"
        ]
        
        # Get test predictions
        X_test = test_df[feature_cols]
        test_preds = model.predict(X_test)
        
        plot_forecast(
            historical_df=features_df,
            test_df=test_df,
            test_preds=test_preds,
            forecast_df=forecast_30d,
            output_path=OUTPUT_DIR / "forecast_plot.png"
        )
    
    return {"outputs_saved": True}
