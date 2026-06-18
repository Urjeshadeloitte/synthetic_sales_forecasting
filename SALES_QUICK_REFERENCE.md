# QUICK REFERENCE - Sales Forecasting Pipeline

## 🚀 Quick Start (30 seconds)

```bash
cd c:\Users\urbakshi\.ms-ad
python -m sales.main
```

Done. Check `sales/output/` for results.

---

## 📋 Common Tasks

### Run the pipeline
```bash
python -m sales.main
```

### Verify everything works
```bash
python verify_sales_pipeline.py
```

### Test reproducibility (byte-identical runs)
```bash
python test_reproducibility.py
```

### Check output details
```bash
python check_outputs.py
```

---

## 🐍 Using in Python Code

### Basic usage
```python
from sales.graph import build_sales_pipeline
from sales.state import SalesState

# Build pipeline
pipeline = build_sales_pipeline()

# Run
state = pipeline.invoke(SalesState())

# Access results
print(state.forecast)           # 30-day forecast DataFrame
print(state.metrics)            # All computed metrics
```

### Access specific results
```python
# Get the forecast
forecast_df = state.forecast
print(f"Forecast for {forecast_df['date'].iloc[0]}: {forecast_df['sales'].iloc[0]:.2f}")

# Get model metrics
print(f"Model R² score: {state.metrics['test_r2']:.4f}")

# Get feature importances
coefs = state.metrics['coefficients']
for feature, weight in sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
    print(f"{feature}: {weight:.4f}")
```

### Access all data
```python
# Raw 180-day data
raw = state.raw_data
print(f"Raw data shape: {raw.shape}")

# Cleaned data
cleaned = state.cleaned_data
print(f"Cleaned data records: {len(cleaned)}")

# Features (14 engineered)
features = state.features_data
print(f"Features shape: {features.shape}")
print(f"Feature columns: {list(features.columns)}")

# Forecast (30 days)
forecast = state.forecast
print(f"Forecast average: {forecast['sales'].mean():.2f}")

# Model object
model = state.model
print(f"Model intercept: {model.intercept_:.2f}")
```

---

## 📊 Output Files Reference

### 1. raw_sales.csv
180 days of synthetic data with trend, seasonality, and noise

```
date,sales
2025-12-18,107.52
2025-12-19,99.28
2025-12-20,130.44
...
2026-06-15,157.23
```

### 2. cleaned_sales.csv
Same as raw (no outliers in this synthetic data)

### 3. features_engineered.csv
Raw data plus 10 key engineered features

```
date,sales,day_of_week,day_of_month,day_of_year,week_of_year,is_weekend,sales_lag_1,sales_lag_7,sales_lag_30,sales_rolling_7,sales_rolling_30
2025-12-18,107.52,3,18,352,51,0,NaN,NaN,NaN,NaN,NaN
```

### 4. forecast_30d.csv
30-day forecast with date and predicted sales

```
date,sales
2026-06-16,167.54
2026-06-17,171.19
2026-06-18,185.15
```

### 5. forecast_plot.png
Line plot showing historical data + forecast (1389×590 pixels)

---

## 🔧 Customization

### Change number of historical days
Edit `sales/config.py`:
```python
HISTORICAL_DAYS = 365  # Instead of 180
```

### Change forecast horizon
Edit `sales/config.py`:
```python
FORECAST_DAYS = 90  # Instead of 30
```

### Change output directory
Edit `sales/config.py`:
```python
OUTPUT_DIR = "forecasts/sales_2024"
CSV_RAW = "forecasts/sales_2024/raw.csv"
# Update other paths...
```

### Disable PNG generation
Edit `sales/nodes/output.py`, comment out:
```python
# plot_forecast(state.cleaned_data, state.forecast, config.PNG_FORECAST)
```

---

## 🧮 Model Details

### Features Used (14 total)

| Type | Feature | Example |
|------|---------|---------|
| **Time** | day_of_week | 0-6 (Mon-Sun) |
| **Time** | day_of_month | 1-31 |
| **Time** | day_of_year | 1-365 |
| **Time** | week_of_year | 1-52 |
| **Time** | is_weekend | 0 or 1 |
| **Lag** | sales_lag_1 | Previous day sales |
| **Lag** | sales_lag_7 | Sales 7 days ago |
| **Lag** | sales_lag_30 | Sales 30 days ago |
| **Rolling** | sales_rolling_7 | 7-day moving average |
| **Rolling** | sales_rolling_30 | 30-day moving average |
| **Trig** | day_of_week_sin | Weekly cycle |
| **Trig** | day_of_week_cos | Weekly cycle |
| **Trig** | day_of_year_sin | Yearly cycle |
| **Trig** | day_of_year_cos | Yearly cycle |

### Model Type
- **Algorithm**: scikit-learn `LinearRegression`
- **Train/Test Split**: 80/20
- **Features**: 14 (listed above)
- **Training Time**: <100ms

### Expected Performance
```
Train MAE:  ~3.9   (Mean Absolute Error)
Test MAE:   ~6.0   (Mean Absolute Error)
Train RMSE: ~4.9   (Root Mean Squared Error)
Test RMSE:  ~7.6   (Root Mean Squared Error)
Train R²:   ~0.96  (Explains 96% of variance)
Test R²:    ~0.73  (Explains 73% of variance)
```

---

## 📈 Synthetic Data Components

The generated data combines:

```
Sales = Trend + Weekly Seasonality + Monthly Effects + Noise

Where:
  Trend = 100 + 0.5 × day (linear growth)
  Weekly = 15 × sin(2π × day / 7) (7-day cycle)
  Monthly = 10 × sin(2π × day / 30) (30-day cycle)
  Noise = N(0, 5) (Gaussian noise)
```

### Example values:
- Day 0: ~100 (base + components)
- Day 90: ~145 (base + growth)
- Day 180: ~190 (base + growth)

---

## 🔄 Reproducibility

**Important**: All runs produce identical outputs

To verify:
```python
import pandas as pd

# Run 1
pipeline.invoke(SalesState())
df1 = pd.read_csv('sales/output/forecast_30d.csv')

# Run 2
pipeline.invoke(SalesState())
df2 = pd.read_csv('sales/output/forecast_30d.csv')

# Compare
assert df1.equals(df2)  # ✓ Always True
```

Why reproducible?
- ✅ Fixed random seed: `RANDOM_SEED = 42`
- ✅ No random APIs: numpy, sklearn all seeded
- ✅ No external input: dates/data deterministic
- ✅ Pure functions: no side effects

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'langgraph'"
```bash
pip install langgraph
```

### "ModuleNotFoundError: No module named 'sales'"
Ensure you're in the workspace root directory:
```bash
cd c:\Users\urbakshi\.ms-ad
python -m sales.main
```

### Output files not created
Check directory permissions:
```bash
mkdir -p sales/output
```

### Import errors in nodes
Ensure relative imports are correct. Example:
```python
from sales.state import SalesState
from sales import config
```

---

## 📚 File Reference

### Core Files
- `sales/main.py` - Entry point, run this
- `sales/graph.py` - Pipeline definition
- `sales/state.py` - Data container
- `sales/config.py` - Configuration

### Node Files
- `sales/nodes/generate.py` - Create 180-day data
- `sales/nodes/clean.py` - Validate & clean
- `sales/nodes/features.py` - Engineer 14 features
- `sales/nodes/train.py` - Train model
- `sales/nodes/forecast.py` - Forecast 30 days
- `sales/nodes/output.py` - Save outputs

### Utility Files
- `sales/utils/plotting.py` - Create PNG plot
- `sales/utils/reporting.py` - Print metrics

### Output Files
- `sales/output/raw_sales.csv` - 180 historical
- `sales/output/cleaned_sales.csv` - After cleaning
- `sales/output/features_engineered.csv` - With features
- `sales/output/forecast_30d.csv` - 30-day forecast
- `sales/output/forecast_plot.png` - Visualization

---

## 🎯 Next Steps

1. **Run it**: `python -m sales.main`
2. **Check outputs**: `python check_outputs.py`
3. **Test reproducibility**: `python test_reproducibility.py`
4. **Explore results**: Look in `sales/output/`
5. **Customize**: Edit `sales/config.py` for different parameters
6. **Integrate**: Import and use in your own code

---

## 📞 Getting Help

1. **See detailed docs**: Open [sales/PACKAGE_GUIDE.md](sales/PACKAGE_GUIDE.md)
2. **Full implementation report**: See [SALES_IMPLEMENTATION_REPORT.md](SALES_IMPLEMENTATION_REPORT.md)
3. **Check code comments**: Every function has docstrings
4. **Run verification**: `python verify_sales_pipeline.py`

---

**Everything is ready to go. Run `python -m sales.main` to get started!**
