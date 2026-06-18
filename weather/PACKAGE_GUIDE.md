# Weather Package Quick Reference

## Running the Pipeline

```bash
# From workspace root
python weather/main.py

# Or directly import
from weather import graph
result = graph.invoke({})
```

## Pipeline Flow

```
raw_weather (list of dicts)
    ↓ [clean_weather]
cleaned_weather (list of dicts, clipped)
    ↓ [engineer_features]
features_df (pandas.DataFrame, 150 rows)
    ↓ [train_model]
model (sklearn.linear_model.LinearRegression)
    ↓ [forecast_next_30_days]
forecast_30d (pandas.DataFrame, 30 rows)
    ↓ [calculate_metrics]
metrics (dict: rmse, mae, r2, etc.)
    ↓ [save_outputs]
Output files in weather/output/
```

## State Schema (weather/state.py)

```python
class PipelineState(TypedDict, total=False):
    raw_weather: list[dict[str, Any]]           # Generated data
    cleaned_weather: list[dict[str, Any]]       # Validated data
    features_df: pd.DataFrame                   # 150 rows, 14 columns
    train_test_split: dict[str, pd.DataFrame]  # "train" & "test" keys
    model: LinearRegression                     # Fitted model
    forecast_30d: pd.DataFrame                  # 30 predictions
    metrics: dict[str, float]                   # RMSE, MAE, R²
    outputs_saved: bool                         # Flag
```

## Node Functions (weather/nodes/)

| Module | Function | Input | Output |
|--------|----------|-------|--------|
| generate.py | `generate_weather_data()` | Empty state | `raw_weather` |
| clean.py | `clean_weather()` | `raw_weather` | `cleaned_weather` |
| features.py | `engineer_features()` | `cleaned_weather` | `features_df` |
| train.py | `train_model()` | `features_df` | `model`, `train_test_split` |
| forecast.py | `forecast_next_30_days()` | `model`, `features_df` | `forecast_30d` |
| metrics.py | `calculate_metrics()` | `model`, `train_test_split` | `metrics` |
| output.py | `save_outputs()` | All state | Writes 5 files |

## Configuration (weather/config.py)

```python
RANDOM_SEED = 42                      # For reproducibility
START_DATE = datetime(2024, 1, 1)    # First day
N_HISTORICAL_DAYS = 180              # Total days generated
N_FORECAST_DAYS = 30                 # Future forecast
TRAIN_TEST_SPLIT_DAY = 150           # Training/test boundary
WEATHER_RANGES = {                   # Validation bounds
    "temp": {"min": -10, "max": 40},
    "humidity": {"min": 0, "max": 100},
    # ... more ...
}
MA_7_DAYS = 7
MA_30_DAYS = 30
OUTPUT_DIR = Path(__file__).parent / "output"
```

## Utility Modules (weather/utils/)

### plotting.py
```python
def plot_forecast(historical_df, test_df, test_preds, forecast_df, output_path)
```
Creates PNG with 4 segments: historical (blue), test actual (green), test predicted (red), forecast (orange)

### reporting.py
```python
def print_pipeline_summary(state: PipelineState) -> None
```
Prints formatted console table with data splits, metrics, forecast stats, output files list

## Data Specifications

### raw_weather format
```python
[
    {
        "date": "2024-01-01",
        "temp": 18.5,        # °C
        "humidity": 65.0,    # %
        "precip": 2.1,       # mm
        "windspeed": 8.3,    # m/s
        "pressure": 1013.2,  # hPa
    },
    # ... 180 days total ...
]
```

### features_df format
```
     date  temp  humidity  precip  windspeed  pressure  day_of_year  sin_doy  cos_doy  temp_mean  temp_ma_7d  temp_ma_30d  precip_ma_7d  humidity_ma_7d
0    2024-01-31  ...
1    2024-02-01  ...
...
150  2024-06-29  ...  (last row after dropping first 30)
```

### forecast_30d format
```
      date          predicted_temp  day_of_year  temp  precip  humidity
0     2024-06-29    14.087          181         14.471  3.930  65.979
1     2024-06-30    13.977          182         12.609  8.146  61.758
...
29    2024-07-28    5.234           211         4.501  6.123  48.321
```

## Feature Engineering Details

**Seasonal Encoding:**
- `sin_doy = sin(2π × day_of_year / 365)` — captures cyclic pattern
- `cos_doy = cos(2π × day_of_year / 365)` — orthogonal component

**Rolling Averages:**
- Computed on 7-day and 30-day windows
- First 30 days dropped due to NaN from 30-day MA initialization

**Target Variable:**
- `temp_mean = temp` (daily temperature becomes target for next day prediction)

## Model Details

**Algorithm:** LinearRegression (sklearn)

**Features (11 total):**
1. day_of_year
2. sin_doy
3. cos_doy
4. humidity
5. precip
6. windspeed
7. pressure
8. temp_ma_7d
9. temp_ma_30d
10. precip_ma_7d
11. humidity_ma_7d

**Training Data:**
- 120 samples (days 30-149, after dropping first 30)
- No validation set; uses test set for metrics

**Test Data:**
- 30 samples (days 150-179)
- Used for RMSE, MAE, R² calculation

## Metrics Definitions

| Metric | Formula | Range | Good |
|--------|---------|-------|------|
| RMSE | √(MSE) | ≥0 | Lower |
| MAE | Σ\|y_true - y_pred\| / n | ≥0 | Lower |
| R² | 1 - (SS_res / SS_tot) | [-∞, 1] | Higher |

## Determinism Checklist

✓ Fixed numpy seed (42) in generation phase
✓ Fixed seed offset (42 + 1000 + day) in forecast phase
✓ LinearRegression is fully deterministic
✓ No random forest, boosting, or stochastic SGD
✓ No dropout, batch norm, or other random regularization
✓ No external API calls or random network operations
✓ No threading or multiprocessing
✓ Date calculations from fixed START_DATE

**Result:** Byte-identical output across runs verified

## Extending

### Add Custom Metric
In metrics.py, add to `metrics` dict:
```python
custom_metric = some_calculation(y_test, y_pred)
metrics["custom_metric"] = custom_metric
```

### Replace Model
In train.py, swap LinearRegression:
```python
# from sklearn.ensemble import RandomForestRegressor  # ❌ Non-deterministic
from sklearn.linear_model import Ridge  # ✓ Deterministic
model = Ridge(alpha=1.0)  # Must keep seed/random_state=None or fixed
```

### Add New Feature
In features.py, after creating DataFrame:
```python
df["my_feature"] = calculation_function(df)
```

Then add to feature_cols in train.py and forecast.py

### Change Data Range
In config.py:
```python
N_HISTORICAL_DAYS = 365  # Increase from 180
N_FORECAST_DAYS = 60     # Increase from 30
TRAIN_TEST_SPLIT_DAY = 300  # Adjust split point
```

## Common Issues & Solutions

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Missing dependencies | `pip install -r requirements.txt` |
| Different results on re-run | Random seed not set | Check config.py RANDOM_SEED |
| Empty output directory | save_outputs failed | Check console for errors |
| Poor R² score (negative) | Model underfitting | Add more features or use different model |
| PNG file truncated | Plotting error | Check matplotlib version |

## Testing

To test determinism:
```bash
# Run 1
python weather/main.py > run1.txt 2>&1

# Run 2
python weather/main.py > run2.txt 2>&1

# Compare
diff run1.txt run2.txt
# Should show no differences (warnings may differ due to timing)
```

To test individual nodes:
```python
from weather.nodes.generate import generate_weather_data
from weather.state import PipelineState

state = {}
result = generate_weather_data(state)
print(f"Generated {len(result['raw_weather'])} days of weather")
```

## Performance Notes

- **Slowest node**: feature engineering (rolling calculations)
- **Fastest node**: forecast (mostly vectorized operations)
- **Total time**: ~2-3 seconds
- **Memory peak**: ~100 MB during feature calculations

## Version Info

- Python: 3.8+
- LangGraph: 0.0.1+
- Pandas: 1.5.0+
- NumPy: 1.23.0+
- scikit-learn: 1.0.0+
- Matplotlib: 3.5.0+
