"""Reporting utilities for metrics and summaries."""
from typing import Dict, Any


def print_metrics(metrics: Dict[str, Any]) -> None:
    """
    Print pipeline metrics to console in a structured format.
    
    Parameters:
    -----------
    metrics : Dict[str, Any]
        Dictionary containing all metrics computed during pipeline execution
    """
    print("\n" + "="*80)
    print("SALES FORECASTING PIPELINE - METRICS REPORT")
    print("="*80)
    
    # Data pipeline metrics
    print("\n[DATA PIPELINE]")
    print(f"  Outliers Removed:              {metrics.get('outliers_removed', 'N/A')}")
    print(f"  Final Record Count:            {metrics.get('final_record_count', 'N/A')}")
    print(f"  Features Engineered:           {metrics.get('features_count', 'N/A')}")
    
    # Model metrics
    print("\n[MODEL PERFORMANCE]")
    print(f"  Train MAE:                     {metrics.get('train_mae', 'N/A'):.4f}")
    print(f"  Test MAE:                      {metrics.get('test_mae', 'N/A'):.4f}")
    print(f"  Train RMSE:                    {metrics.get('train_rmse', 'N/A'):.4f}")
    print(f"  Test RMSE:                     {metrics.get('test_rmse', 'N/A'):.4f}")
    print(f"  Train R²:                      {metrics.get('train_r2', 'N/A'):.4f}")
    print(f"  Test R²:                       {metrics.get('test_r2', 'N/A'):.4f}")
    print(f"  Model Intercept:               {metrics.get('intercept', 'N/A'):.4f}")
    
    # Forecast metrics
    print("\n[FORECAST]")
    print(f"  Forecast Records:              {metrics.get('forecast_records', 'N/A')}")
    
    # Output files
    print("\n[OUTPUT FILES]")
    print(f"  Raw CSV:                       {metrics.get('raw_csv', 'N/A')}")
    print(f"  Cleaned CSV:                   {metrics.get('cleaned_csv', 'N/A')}")
    print(f"  Features CSV:                  {metrics.get('features_csv', 'N/A')}")
    print(f"  Forecast CSV:                  {metrics.get('forecast_csv', 'N/A')}")
    print(f"  Forecast Plot (PNG):           {metrics.get('forecast_plot', 'N/A')}")
    
    # Top feature coefficients
    if 'coefficients' in metrics and metrics['coefficients']:
        print("\n[TOP 10 FEATURE COEFFICIENTS]")
        coef_dict = metrics['coefficients']
        sorted_coefs = sorted(coef_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
        for feat, coef in sorted_coefs:
            print(f"  {feat:.<35} {coef:>12.6f}")
    
    print("\n" + "="*80 + "\n")
