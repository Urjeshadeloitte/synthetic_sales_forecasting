"""Reporting utilities for console output."""

from weather.state import PipelineState


def print_pipeline_summary(state: PipelineState) -> None:
    """
    Print a formatted summary of the pipeline execution and results to console.
    
    Args:
        state: Final PipelineState after all nodes have executed
    """
    metrics = state.get("metrics", {})
    train_test_split = state.get("train_test_split", {})
    
    # Get data sizes
    train_size = len(train_test_split.get("train", [])) if train_test_split else 0
    test_size = len(train_test_split.get("test", [])) if train_test_split else 0
    
    # Extract metrics
    rmse = metrics.get("rmse", 0)
    mae = metrics.get("mae", 0)
    r2 = metrics.get("r2", 0)
    mean_pred = metrics.get("mean_pred", 0)
    std_pred = metrics.get("std_pred", 0)
    min_pred = metrics.get("min_pred", 0)
    max_pred = metrics.get("max_pred", 0)
    
    print("\n" + "=" * 60)
    print("    Weather Forecast Pipeline Summary")
    print("=" * 60)
    
    print(f"\nData Splits:")
    print(f"  Training Data:  {train_size} samples")
    print(f"  Test Data:      {test_size} samples")
    print(f"  Forecast:       30 days")
    
    print(f"\nModel Performance (Test Set):")
    print(f"  RMSE:           {rmse:.3f} °C")
    print(f"  MAE:            {mae:.3f} °C")
    print(f"  R² Score:       {r2:.3f}")
    
    print(f"\nForecast Statistics:")
    print(f"  Mean Temperature: {mean_pred:.2f} °C")
    print(f"  Std Deviation:    {std_pred:.2f} °C")
    print(f"  Range:            [{min_pred:.2f}, {max_pred:.2f}] °C")
    
    print(f"\nOutputs saved to: weather/output/")
    print(f"  - raw_weather.csv")
    print(f"  - cleaned_weather.csv")
    print(f"  - features_engineered.csv")
    print(f"  - forecast_30d.csv")
    print(f"  - forecast_plot.png")
    
    print("\n" + "=" * 60)
