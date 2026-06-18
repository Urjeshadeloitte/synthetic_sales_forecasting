"""Verification script for the sales pipeline."""
import sys
from sales.graph import build_sales_pipeline
from sales.state import SalesState
from sales import config
import os
import pandas as pd


def verify_pipeline():
    """
    Verify the sales pipeline runs successfully and produces expected outputs.
    """
    print("Verifying Sales Forecasting Pipeline...")
    print("=" * 80)
    
    try:
        # Step 1: Build pipeline
        print("\n[1/3] Building pipeline...", end=" ")
        pipeline = build_sales_pipeline()
        print("✓")
        
        # Step 2: Execute pipeline
        print("[2/3] Executing pipeline...", end=" ")
        initial_state = SalesState()
        final_state = pipeline.invoke(initial_state)
        print("✓")
        
        # Step 3: Verify outputs
        print("[3/3] Verifying outputs...", end=" ")
        
        # Check CSV files exist
        required_files = [
            config.CSV_RAW,
            config.CSV_CLEANED,
            config.CSV_FEATURES,
            config.CSV_FORECAST,
            config.PNG_FORECAST
        ]
        
        for filepath in required_files:
            if not os.path.exists(filepath):
                print(f"\n✗ Missing: {filepath}")
                return False
        
        # Verify data integrity
        forecast_df = pd.read_csv(config.CSV_FORECAST)
        if len(forecast_df) != config.FORECAST_DAYS:
            print(f"\n✗ Forecast has {len(forecast_df)} records, expected {config.FORECAST_DAYS}")
            return False
        
        print("✓")
        
        print("\n" + "=" * 80)
        print("VERIFICATION SUCCESSFUL!")
        print("=" * 80)
        print(f"\nAll outputs verified in: {config.OUTPUT_DIR}/")
        print("  - raw_sales.csv")
        print("  - cleaned_sales.csv")
        print("  - features_engineered.csv")
        print("  - forecast_30d.csv")
        print("  - forecast_plot.png")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_pipeline()
    sys.exit(0 if success else 1)
