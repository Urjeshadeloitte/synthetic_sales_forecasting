"""Test reproducibility of the pipeline."""
import pandas as pd
import os
import shutil
from datetime import datetime

# Backup first run
print("Backing up first run outputs...")
os.makedirs('sales/output_backup1', exist_ok=True)
for file in os.listdir('sales/output'):
    if file.endswith('.csv'):
        shutil.copy(f'sales/output/{file}', f'sales/output_backup1/{file}')

# Read first outputs
df1_forecast = pd.read_csv('sales/output/forecast_30d.csv')
df1_raw = pd.read_csv('sales/output/raw_sales.csv')
df1_cleaned = pd.read_csv('sales/output/cleaned_sales.csv')

print("Running pipeline second time...")
from sales.main import main
main()

# Read second outputs
df2_forecast = pd.read_csv('sales/output/forecast_30d.csv')
df2_raw = pd.read_csv('sales/output/raw_sales.csv')
df2_cleaned = pd.read_csv('sales/output/cleaned_sales.csv')

# Compare
print("\n" + "="*80)
print("REPRODUCIBILITY TEST")
print("="*80)

# Compare forecasts
forecast_identical = df1_forecast.equals(df2_forecast)
print(f"\nForecast identical: {forecast_identical}")
if not forecast_identical:
    print("First 3 rows of run 1:")
    print(df1_forecast.head(3))
    print("First 3 rows of run 2:")
    print(df2_forecast.head(3))
    
# Compare raw data
raw_identical = df1_raw.equals(df2_raw)
print(f"Raw data identical: {raw_identical}")

# Compare cleaned data
cleaned_identical = df1_cleaned.equals(df2_cleaned)
print(f"Cleaned data identical: {cleaned_identical}")

if forecast_identical and raw_identical and cleaned_identical:
    print("\n✓ REPRODUCIBILITY TEST PASSED!")
    print("✓ All outputs are byte-identical across runs")
else:
    print("\n✗ Reproducibility issue detected")

print("\nFirst run backups saved to: sales/output_backup1/")
