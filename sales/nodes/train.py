"""Node: Train LinearRegression model."""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sales.state import SalesState
from sales import config


def train_model(state: SalesState) -> SalesState:
    """
    Train scikit-learn LinearRegression model.
    
    Features: all columns except 'date' and 'sales'
    Target: 'sales'
    
    Computes train/test metrics (80/20 split).
    """
    np.random.seed(config.RANDOM_SEED)
    
    df = state.features_data.copy()
    
    # Prepare feature matrix and target
    feature_cols = [col for col in df.columns if col not in ['date', 'sales']]
    X = df[feature_cols].values
    y = df['sales'].values
    
    # Train/test split
    split_idx = int(len(df) * (1 - config.TEST_SIZE))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions and metrics
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    state.model = model
    state.metrics['train_mae'] = train_mae
    state.metrics['test_mae'] = test_mae
    state.metrics['train_rmse'] = train_rmse
    state.metrics['test_rmse'] = test_rmse
    state.metrics['train_r2'] = train_r2
    state.metrics['test_r2'] = test_r2
    state.metrics['feature_names'] = feature_cols
    state.metrics['coefficients'] = dict(zip(feature_cols, model.coef_))
    state.metrics['intercept'] = model.intercept_
    
    return state
