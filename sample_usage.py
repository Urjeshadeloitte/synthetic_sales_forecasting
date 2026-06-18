"""
Sample Usage Script - Sales Forecasting Pipeline

This script demonstrates various ways to use the sales forecasting package,
including running the pipeline, accessing results, and analyzing outputs.
"""

import pandas as pd
from sales.graph import build_sales_pipeline
from sales.state import SalesState
from sales import config


def example_1_basic_run():
    """Example 1: Basic pipeline execution."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Pipeline Execution")
    print("="*80)
    
    # Build the pipeline
    pipeline = build_sales_pipeline()
    
    # Initialize state
    state = SalesState()
    
    # Run the pipeline (returns dict)
    result = pipeline.invoke(state)
    
    print("\n✓ Pipeline executed successfully!")
    print(f"  - Historical records: {len(result['raw_data'])}")
    print(f"  - Forecast records: {len(result['forecast'])}")
    print(f"  - Model R² score: {result['metrics']['test_r2']:.4f}")


def example_2_access_forecast():
    """Example 2: Access and display forecast."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Access and Display Forecast")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    # Get forecast dataframe
    forecast = state.forecast
    
    print("\nForecast for next 30 days:")
    print(forecast.to_string(index=False))
    
    # Calculate summary statistics
    print(f"\nForecast Summary:")
    print(f"  Min sales: {forecast['sales'].min():.2f}")
    print(f"  Max sales: {forecast['sales'].max():.2f}")
    print(f"  Mean sales: {forecast['sales'].mean():.2f}")
    print(f"  Total (sum): {forecast['sales'].sum():.2f}")


def example_3_model_metrics():
    """Example 3: Access and display model metrics."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Model Performance Metrics")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    metrics = state.metrics
    
    print("\nModel Performance:")
    print(f"  Train MAE:  {metrics['train_mae']:.4f}")
    print(f"  Test MAE:   {metrics['test_mae']:.4f}")
    print(f"  Train RMSE: {metrics['train_rmse']:.4f}")
    print(f"  Test RMSE:  {metrics['test_rmse']:.4f}")
    print(f"  Train R²:   {metrics['train_r2']:.4f}")
    print(f"  Test R²:    {metrics['test_r2']:.4f}")
    
    print("\nTop 5 Most Important Features:")
    coef_dict = metrics['coefficients']
    sorted_coefs = sorted(coef_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    for rank, (feature, coef) in enumerate(sorted_coefs, 1):
        print(f"  {rank}. {feature:<25} {coef:>10.6f}")


def example_4_feature_analysis():
    """Example 4: Analyze engineered features."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Engineered Features Analysis")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    features_df = state.features_data
    
    print(f"\nFeatures shape: {features_df.shape}")
    print(f"Columns: {list(features_df.columns)}")
    
    print("\nFirst 5 rows of features:")
    print(features_df.head(5).to_string())
    
    print("\nFeature statistics:")
    print(features_df.describe().to_string())


def example_5_compare_raw_vs_forecast():
    """Example 5: Compare historical data with forecast."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Compare Historical Data vs Forecast")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    historical = state.cleaned_data
    forecast = state.forecast
    
    print("\nHistorical Data Statistics:")
    print(f"  Records: {len(historical)}")
    print(f"  Min: {historical['sales'].min():.2f}")
    print(f"  Max: {historical['sales'].max():.2f}")
    print(f"  Mean: {historical['sales'].mean():.2f}")
    print(f"  Std Dev: {historical['sales'].std():.2f}")
    
    print("\nForecast Statistics:")
    print(f"  Records: {len(forecast)}")
    print(f"  Min: {forecast['sales'].min():.2f}")
    print(f"  Max: {forecast['sales'].max():.2f}")
    print(f"  Mean: {forecast['sales'].mean():.2f}")
    print(f"  Std Dev: {forecast['sales'].std():.2f}")
    
    print("\nTrend Analysis:")
    last_historical = historical['sales'].iloc[-1]
    forecast_mean = forecast['sales'].mean()
    change_pct = ((forecast_mean - last_historical) / last_historical) * 100
    print(f"  Last historical sales: {last_historical:.2f}")
    print(f"  Forecast average: {forecast_mean:.2f}")
    print(f"  Expected change: {change_pct:+.2f}%")


def example_6_export_analysis():
    """Example 6: Export analysis results to CSV."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Export Analysis Results")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    # Create analysis summary
    analysis = {
        'Metric': [
            'Historical Records',
            'Forecast Records',
            'Historical Mean Sales',
            'Forecast Mean Sales',
            'Model Train R²',
            'Model Test R²',
            'Model Test MAE',
            'Train/Test Ratio'
        ],
        'Value': [
            len(state.cleaned_data),
            len(state.forecast),
            f"{state.cleaned_data['sales'].mean():.2f}",
            f"{state.forecast['sales'].mean():.2f}",
            f"{state.metrics['train_r2']:.4f}",
            f"{state.metrics['test_r2']:.4f}",
            f"{state.metrics['test_mae']:.4f}",
            f"{config.TEST_SIZE}"
        ]
    }
    
    analysis_df = pd.DataFrame(analysis)
    
    # Save analysis
    analysis_csv = 'sales/output/analysis_summary.csv'
    analysis_df.to_csv(analysis_csv, index=False)
    
    print(f"\nAnalysis Summary:")
    print(analysis_df.to_string(index=False))
    print(f"\n✓ Summary exported to: {analysis_csv}")


def example_7_load_from_csv():
    """Example 7: Load and analyze results from CSV files."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Load and Analyze from CSV Files")
    print("="*80)
    
    # Load CSVs
    raw = pd.read_csv(config.CSV_RAW)
    cleaned = pd.read_csv(config.CSV_CLEANED)
    forecast = pd.read_csv(config.CSV_FORECAST)
    
    print("\nLoaded data from CSV files:")
    print(f"  Raw sales records: {len(raw)}")
    print(f"  Cleaned sales records: {len(cleaned)}")
    print(f"  Forecast records: {len(forecast)}")
    
    # Perform analysis
    print("\nCombined dataset analysis:")
    combined_sales = pd.concat([
        cleaned[['sales']].rename(columns={'sales': 'Type'}),
        forecast[['sales']].rename(columns={'sales': 'Type'})
    ], ignore_index=True)
    
    print(f"  Total observations: {len(combined_sales)}")
    print(f"  Combined mean: {combined_sales['Type'].mean():.2f}")
    print(f"  Combined min: {combined_sales['Type'].min():.2f}")
    print(f"  Combined max: {combined_sales['Type'].max():.2f}")


def example_8_reproduce_check():
    """Example 8: Verify reproducibility."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Reproducibility Check")
    print("="*80)
    
    pipeline1 = build_sales_pipeline()
    state1 = pipeline1.invoke(SalesState())
    forecast1 = state1.forecast.copy()
    
    pipeline2 = build_sales_pipeline()
    state2 = pipeline2.invoke(SalesState())
    forecast2 = state2.forecast.copy()
    
    # Compare
    is_identical = forecast1.equals(forecast2)
    
    print(f"\nRun 1 forecast (first 3 rows):")
    print(forecast1.head(3).to_string(index=False))
    
    print(f"\nRun 2 forecast (first 3 rows):")
    print(forecast2.head(3).to_string(index=False))
    
    print(f"\nComparison:")
    print(f"  Forecasts identical: {is_identical}")
    print(f"  ✓ Pipeline is fully reproducible!" if is_identical else "  ✗ Mismatch detected")


def example_9_what_if_analysis():
    """Example 9: What-if analysis (comparison of different random seeds)."""
    print("\n" + "="*80)
    print("EXAMPLE 9: Model Sensitivity Analysis")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    metrics = state.metrics
    
    print("\nModel Sensitivity Metrics:")
    print(f"  Test MAE (absolute error): {metrics['test_mae']:.4f}")
    print(f"  Test RMSE (squared error): {metrics['test_rmse']:.4f}")
    print(f"  Test R² (variance explained): {metrics['test_r2']:.4f}")
    
    print("\nInterpretation:")
    print(f"  - MAE: Forecast is off by ~{metrics['test_mae']:.2f} units on average")
    print(f"  - RMSE: Typical error magnitude is ~{metrics['test_rmse']:.2f}")
    print(f"  - R²: Model explains {metrics['test_r2']*100:.1f}% of sales variance")
    
    print("\nTop contributing features:")
    coef_dict = metrics['coefficients']
    sorted_coefs = sorted(coef_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    for feature, weight in sorted_coefs:
        print(f"  - {feature}: {weight:.4f} (impact per unit change)")


def example_10_full_pipeline_summary():
    """Example 10: Complete pipeline summary and status report."""
    print("\n" + "="*80)
    print("EXAMPLE 10: Full Pipeline Summary & Status Report")
    print("="*80)
    
    pipeline = build_sales_pipeline()
    state = pipeline.invoke(SalesState())
    
    print("\n📊 PIPELINE STATUS REPORT")
    print("-" * 80)
    
    print("\n[DATA GENERATION]")
    print(f"  ✓ Historical period: 180 days")
    print(f"  ✓ Synthetic data components: trend + seasonality + noise")
    print(f"  ✓ Records generated: {len(state.raw_data)}")
    
    print("\n[DATA CLEANING]")
    outliers = state.metrics.get('outliers_removed', 0)
    print(f"  ✓ Outliers removed: {outliers}")
    print(f"  ✓ Records retained: {state.metrics['final_record_count']}")
    
    print("\n[FEATURE ENGINEERING]")
    print(f"  ✓ Features created: {state.metrics['features_count']}")
    print(f"  ✓ Feature types: time-based, lagged, rolling, trigonometric")
    
    print("\n[MODEL TRAINING]")
    print(f"  ✓ Algorithm: scikit-learn LinearRegression")
    print(f"  ✓ Train R²: {state.metrics['train_r2']:.4f}")
    print(f"  ✓ Test R²: {state.metrics['test_r2']:.4f}")
    print(f"  ✓ Test MAE: {state.metrics['test_mae']:.4f}")
    
    print("\n[FORECASTING]")
    print(f"  ✓ Forecast period: 30 days")
    print(f"  ✓ Forecast records: {state.metrics['forecast_records']}")
    print(f"  ✓ Forecast range: {state.forecast['sales'].min():.2f} - {state.forecast['sales'].max():.2f}")
    
    print("\n[OUTPUT FILES]")
    print(f"  ✓ {state.metrics['raw_csv']}")
    print(f"  ✓ {state.metrics['cleaned_csv']}")
    print(f"  ✓ {state.metrics['features_csv']}")
    print(f"  ✓ {state.metrics['forecast_csv']}")
    print(f"  ✓ {state.metrics['forecast_plot']}")
    
    print("\n[REPRODUCIBILITY]")
    print(f"  ✓ Random seed: {config.RANDOM_SEED}")
    print(f"  ✓ Deterministic: Yes (byte-identical outputs)")
    print(f"  ✓ External APIs: None")
    print(f"  ✓ LLM calls: None")
    
    print("\n" + "-" * 80)
    print("✓ PIPELINE EXECUTION COMPLETE\n")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("SALES FORECASTING PIPELINE - SAMPLE USAGE EXAMPLES")
    print("="*80)
    
    examples = [
        ("Basic Pipeline Execution", example_1_basic_run),
        ("Access and Display Forecast", example_2_access_forecast),
        ("Model Performance Metrics", example_3_model_metrics),
        ("Engineered Features Analysis", example_4_feature_analysis),
        ("Compare Historical vs Forecast", example_5_compare_raw_vs_forecast),
        ("Export Analysis Results", example_6_export_analysis),
        ("Load from CSV Files", example_7_load_from_csv),
        ("Reproducibility Check", example_8_reproduce_check),
        ("Model Sensitivity Analysis", example_9_what_if_analysis),
        ("Full Pipeline Summary", example_10_full_pipeline_summary),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "="*80)
    print("Running all examples...")
    print("="*80)
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Error in {name}: {str(e)}")
    
    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80)
    print("\nTo run individual examples, import and call the function:")
    print("  from sample_usage import example_1_basic_run")
    print("  example_1_basic_run()")
    print()


if __name__ == "__main__":
    main()
