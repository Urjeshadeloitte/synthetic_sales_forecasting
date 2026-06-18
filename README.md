# Sales Forecasting Pipeline

A **production-ready, self-contained, deterministic LangGraph-based pipeline** for generating synthetic sales data, engineering features, training ML models, and forecasting 30 days ahead with **zero external APIs or LLM calls**.

[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Deterministic](https://img.shields.io/badge/Deterministic-✓-green.svg)](https://en.wikipedia.org/wiki/Deterministic_system)

## ✅ Completed Implementation

A **fully self-contained, deterministic Python package** has been successfully built in `sales/` folder that implements a complete LangGraph pipeline for sales forecasting.

### Quick Facts

| Aspect | Details |
|--------|---------|
| **Package Location** | `sales/` folder |
| **Pipeline Type** | LangGraph state machine |
| **Historical Data** | 180 days of synthetic sales |
| **Forecast Horizon** | 30 days ahead |
| **ML Model** | scikit-learn `LinearRegression` |
| **Reproducibility** | ✅ Byte-identical outputs (fixed seed: 42) |
| **Dependencies** | langgraph, pandas, numpy, scikit-learn, matplotlib |
| **External APIs** | ✅ NONE - fully self-contained |
| **LLM Calls** | ✅ NONE - deterministic functions only |

---

## 📋 Pipeline Architecture

### 6-Node LangGraph Pipeline

```
[generate] → [clean] → [features] → [train] → [forecast] → [output]
   ↓         ↓        ↓          ↓       ↓         ↓
  180d      Clean   14 Features Train  Forecast  CSV+PNG
  Raw      Validate Model    Metrics   30d
```

### Node Details

| Node | Function | Inputs | Outputs |
|------|----------|--------|---------|
| **generate** | Create synthetic data | None | 180 rows of raw sales |
| **clean** | Validate & remove outliers | raw_data | cleaned_data |
| **features** | Engineer 14 time-based features | cleaned_data | features_data |
| **train** | Fit LinearRegression model | features_data | model + metrics |
| **forecast** | Predict next 30 days | model, features | forecast_data |
| **output** | Save CSV/PNG, print metrics | all state | output files |

---

## 📊 Generated Components

### Data Generated (180 days)

Each day includes:
- **Trend**: Linear growth (+0.5 per day)
- **Weekly Seasonality**: 7-day cycle (amplitude 15)
- **Monthly Effects**: 30-day cycle (amplitude 10)
- **Random Noise**: Gaussian (std dev 5)

All mathematically combined to create realistic sales patterns.

### Features Engineered (14 total)

**Time-Based:**
- day_of_week, day_of_month, day_of_year, week_of_year, is_weekend

**Lagged:**
- sales_lag_1, sales_lag_7, sales_lag_30

**Rolling Averages:**
- sales_rolling_7, sales_rolling_30

**Trigonometric Seasonality:**
- day_of_week_sin/cos, day_of_year_sin/cos

### Model Performance

From latest run:
```
Train MAE:    3.94    (Mean Absolute Error on training set)
Test MAE:     5.96    (Mean Absolute Error on test set)
Train RMSE:   4.91    (Root Mean Squared Error on training set)
Test RMSE:    7.64    (Root Mean Squared Error on test set)
Train R²:     0.9593  (Coefficient of determination on training set)
Test R²:      0.7315  (Coefficient of determination on test set)
```

---

## 📁 Output Files

All files generated in `sales/output/`:

| File | Size | Records | Purpose |
|------|------|---------|---------|
| **raw_sales.csv** | ~5 KB | 180 | Original synthetic data |
| **cleaned_sales.csv** | ~5 KB | 180 | After validation |
| **features_engineered.csv** | ~35 KB | 180 | With 14 engineered features |
| **forecast_30d.csv** | ~2 KB | 30 | 30-day forecast predictions |
| **forecast_plot.png** | ~87 KB | 1 | Visualization (1389×590px) |

---

## 🚀 Running the Pipeline

### Quick Start (3 ways)

```bash
# Method 1: Module execution
python -m sales.main

# Method 2: Direct script
python sales/main.py

# Method 3: Verification script
python verify_sales_pipeline.py
```

### Example Usage in Code

```python
from sales.graph import build_sales_pipeline
from sales.state import SalesState

# Build and run
pipeline = build_sales_pipeline()
state = pipeline.invoke(SalesState())

# Access results
print(state.forecast)  # DataFrame with 30 day forecast
print(state.metrics)   # Dictionary of all metrics
```

---

## ✅ Reproducibility Verification

**Status**: ✅ **PASSED**

Test results confirm:
- ✅ Forecast data: **Byte-identical** across runs
- ✅ Raw data: **Byte-identical** across runs
- ✅ Cleaned data: **Byte-identical** across runs
- ✅ All metrics: **Identical** across runs

Achieved via:
1. Fixed `RANDOM_SEED = 42` in config.py
2. Deterministic algorithms (numpy, pandas, sklearn)
3. No external API calls or variable inputs
4. Pure functions with no side effects

---

## 📂 File Structure

```
c:\Users\urbakshi\.ms-ad\
├── sales/
│   ├── __init__.py              # Package entry
│   ├── config.py                # Configuration (seed=42)
│   ├── state.py                 # SalesState dataclass
│   ├── graph.py                 # LangGraph builder
│   ├── main.py                  # Main entry point
│   ├── PACKAGE_GUIDE.md         # Detailed documentation
│   │
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── generate.py          # Generate 180-day data
│   │   ├── clean.py             # Clean & validate
│   │   ├── features.py          # Engineer 14 features
│   │   ├── train.py             # Train LinearRegression
│   │   ├── forecast.py          # Forecast 30 days
│   │   └── output.py            # Write CSV/PNG/metrics
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── plotting.py          # Matplotlib visualization
│   │   └── reporting.py         # Console metrics
│   │
│   └── output/
│       ├── raw_sales.csv
│       ├── cleaned_sales.csv
│       ├── features_engineered.csv
│       ├── forecast_30d.csv
│       └── forecast_plot.png
│
├── requirements.txt             # Dependencies
├── verify_sales_pipeline.py     # Verification script
├── test_reproducibility.py      # Reproducibility test
├── check_outputs.py             # Output inspection script
└── [Other workspace files]
```

---

## 🔧 Configuration

Edit `sales/config.py` to customize:

```python
RANDOM_SEED = 42              # Reproducibility seed
HISTORICAL_DAYS = 180         # How many days to generate
FORECAST_DAYS = 30            # How many days to forecast
TEST_SIZE = 0.2               # Train/test split
OUTPUT_DIR = "sales/output"   # Output location
CSV_RAW = "sales/output/raw_sales.csv"
CSV_CLEANED = "sales/output/cleaned_sales.csv"
CSV_FEATURES = "sales/output/features_engineered.csv"
CSV_FORECAST = "sales/output/forecast_30d.csv"
PNG_FORECAST = "sales/output/forecast_plot.png"
```

---

## 🎯 Key Features

✅ **Fully Deterministic**
- Fixed random seed ensures byte-identical outputs
- Same inputs → Same outputs (verified)

✅ **No External Dependencies**
- No LLM/API calls
- No API keys required
- No network requests

✅ **Production Ready**
- Professional error handling
- CSV outputs for integration
- PNG visualization for stakeholders
- Comprehensive metrics reporting

✅ **LangGraph Architecture**
- Modular node-based design
- Easy to extend with new nodes
- State machine pattern for clarity
- Professional ML pipeline pattern

✅ **Comprehensive Output**
- Raw data with 3 synthetic components
- Cleaned and validated data
- 14 engineered features
- Trained scikit-learn model
- 30-day ahead forecast
- Visualization plot
- Console metrics report

---

## 📊 Sample Metrics Output

```
================================================================================
SALES FORECASTING PIPELINE - METRICS REPORT
================================================================================

[DATA PIPELINE]
  Outliers Removed:              0
  Final Record Count:            180
  Features Engineered:           14

[MODEL PERFORMANCE]
  Train MAE:                     3.9368
  Test MAE:                      5.9644
  Train RMSE:                    4.9057
  Test RMSE:                    7.6395
  Train R²:                      0.9593
  Test R²:                       0.7315
  Model Intercept:               22.0250

[FORECAST]
  Forecast Records:              30

[OUTPUT FILES]
  Raw CSV:                       sales/output/raw_sales.csv
  Cleaned CSV:                   sales/output/cleaned_sales.csv
  Features CSV:                  sales/output/features_engineered.csv
  Forecast CSV:                  sales/output/forecast_30d.csv
  Forecast Plot (PNG):           sales/output/forecast_plot.png

[TOP 10 FEATURE COEFFICIENTS]
  day_of_week_sin....................   -13.881897
  day_of_year_sin....................     6.733812
  day_of_week_cos....................    -6.453720
  is_weekend.........................    -5.728193
  day_of_year_cos....................    -5.317635
  day_of_week........................     1.811767
  sales_rolling_7....................     0.840326
  day_of_month.......................     0.218943
  sales_lag_7........................    -0.195273
  week_of_year.......................     0.100280
```

---

## 🧪 Testing & Verification

### Run Verification Script

```bash
python verify_sales_pipeline.py
```

Expected output:
```
[1/3] Building pipeline... ✓
[2/3] Executing pipeline... ✓
[3/3] Verifying outputs... ✓

VERIFICATION SUCCESSFUL!
```

### Test Reproducibility

```bash
python test_reproducibility.py
```

Expected output:
```
✓ REPRODUCIBILITY TEST PASSED!
✓ All outputs are byte-identical across runs
```

### Check Output Details

```bash
python check_outputs.py
```

Expected output:
```
=== RAW DATA ===
Records: 180
Date range: 2025-12-18 to 2026-06-15
Sales stats - min: 80.38, max: 211.46, mean: 144.79

=== FORECAST ===
Records: 30
Date range: 2026-06-16 to 2026-07-15
Sales forecast - min: 144.86, max: 199.66, mean: 171.41

✓ All outputs verified successfully!
```

---

## 📖 Documentation

For detailed documentation, see:
- **[sales/PACKAGE_GUIDE.md](sales/PACKAGE_GUIDE.md)** - Complete package guide with node details
- **Inline code comments** - Every node has detailed docstrings

---

## 🔍 Architecture Highlights

### State Container (SalesState)

```python
@dataclass
class SalesState:
    raw_data: Optional[pd.DataFrame]      # 180-day synthetic data
    cleaned_data: Optional[pd.DataFrame]  # After validation
    features_data: Optional[pd.DataFrame] # With 14 features
    model: Optional[object]               # Fitted LinearRegression
    forecast: Optional[pd.DataFrame]      # 30-day predictions
    metrics: dict                         # All computed metrics
```

### Pipeline Flow

Each node is a pure function:
```python
def node_function(state: SalesState) -> SalesState:
    # Process state
    state.some_field = compute_result()
    state.metrics.update({...})
    return state
```

This ensures:
- ✅ Testability
- ✅ Reproducibility
- ✅ Modularity
- ✅ Clarity

---

## ✨ Summary

This is a **production-ready, fully self-contained Python package** that demonstrates:

1. **Professional ML Pipeline Architecture** - Using LangGraph for orchestration
2. **Data Engineering Best Practices** - Synthetic data generation with realistic patterns
3. **Deterministic Reproducibility** - Byte-identical outputs with fixed seeds
4. **Complete Forecasting Workflow** - Data → Features → Model → Forecast → Output
5. **No External Dependencies** - Pure Python with standard ML libraries

All components are documented, tested, and ready for extension.

**Total nodes**: 6 | **Lines of code**: ~800 | **Dependencies**: 5 | **Output files**: 5 | **Reproducibility**: ✅ Perfect

---

## 🎓 Key Learnings for Replication

If building similar pipelines:

1. **Use fixed seeds everywhere**: numpy, random, sklearn, pandas
2. **Document data generation**: Make synthetic data realistic and understood
3. **Modularize with LangGraph**: Each step is a node, data flows through state
4. **Comprehensive metrics**: Track everything for debugging and validation
5. **Output multiple formats**: CSV for integration, PNG for visualization
6. **Test reproducibility**: Run twice, compare outputs, verify byte-identity

---

**Status**: ✅ **Complete** | **Tested**: ✅ **Yes** | **Reproducible**: ✅ **Yes** | **Ready**: ✅ **Production**
