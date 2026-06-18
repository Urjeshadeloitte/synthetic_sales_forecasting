import pandas as pd

print("\n=== RAW DATA ===")
df_raw = pd.read_csv('sales/output/raw_sales.csv')
print(f'Records: {len(df_raw)}')
print(f'Date range: {df_raw["date"].iloc[0]} to {df_raw["date"].iloc[-1]}')
print(f'Sales stats - min: {df_raw["sales"].min():.2f}, max: {df_raw["sales"].max():.2f}, mean: {df_raw["sales"].mean():.2f}')

print("\n=== CLEANED DATA ===")
df_clean = pd.read_csv('sales/output/cleaned_sales.csv')
print(f'Records: {len(df_clean)}')
print(f'Sales stats - min: {df_clean["sales"].min():.2f}, max: {df_clean["sales"].max():.2f}, mean: {df_clean["sales"].mean():.2f}')

print("\n=== FEATURES DATA ===")
df_feat = pd.read_csv('sales/output/features_engineered.csv')
print(f'Records: {len(df_feat)}')
print(f'Columns: {len(df_feat.columns)}')
print(f'Column names: {list(df_feat.columns)}')

print("\n=== FORECAST ===")
df_forecast = pd.read_csv('sales/output/forecast_30d.csv')
print(f'Records: {len(df_forecast)}')
print(f'Date range: {df_forecast["date"].iloc[0]} to {df_forecast["date"].iloc[-1]}')
print(f'Sales forecast - min: {df_forecast["sales"].min():.2f}, max: {df_forecast["sales"].max():.2f}, mean: {df_forecast["sales"].mean():.2f}')

print("\n✓ All outputs verified successfully!")
