"""
Module: train_model.py
Purpose: Train a Random Forest regressor on engineered features for retail sales forecasting.
"""

# src/models/train_model.py

import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import joblib
import numpy as np
import mlflow

PROCESSED_PATH = Path("data/processed")
MODEL_PATH = Path("models")
MODEL_FILE = MODEL_PATH / "rf_sales_model.pkl"

def load_data(path=PROCESSED_PATH / "train_features.csv"):
    print("📂 Loading feature data...")
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def prepare_features(df):
    print("🧹 Preparing features and target...")
    target = "Weekly_Sales"
    drop_cols = ["Date", target, "Total_MarkDown", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
    features = [col for col in df.columns if col not in drop_cols]
    return features, target

def split_data(df, features, target):
    print("🧪 Splitting data by time...")
    train_df = df[df["Year"] < 2012]
    test_df = df[df["Year"] == 2012]
    # One-hot encode both train and test, then align columns
    X_train = pd.get_dummies(train_df[features], drop_first=True)
    X_test = pd.get_dummies(test_df[features], drop_first=True)
    X_train, X_test = X_train.align(X_test, join='outer', axis=1, fill_value=0)
    # Cast integer columns to float64 to avoid MLflow schema issues
    for col in X_train.columns:
        if pd.api.types.is_integer_dtype(X_train[col]):
            X_train[col] = X_train[col].astype('float64')
            X_test[col] = X_test[col].astype('float64')
    y_train = train_df[target]
    y_test = test_df[target]
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train, X_val, y_val):
    print("🧠 Training Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        n_jobs=-1,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    print("📊 Evaluating model...")
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"✅ RMSE on test set: {rmse:.2f}")
    print(f"✅ MAE on test set: {mae:.2f}")
    print(f"✅ R2 on test set: {r2:.4f}")
    return {'rmse': rmse, 'mae': mae, 'r2': r2}

def save_model(model, path=MODEL_FILE):
    MODEL_PATH.mkdir(exist_ok=True)
    joblib.dump(model, str(path.with_suffix('.pkl')))
    print(f"💾 Model saved to {path.with_suffix('.pkl')}")

def run_pipeline():
    df = load_data()
    features, target = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(df, features, target)
    with mlflow.start_run(run_name="RandomForest_SalesForecast"):
        model = train_model(X_train, y_train, X_test, y_test)
        metrics = evaluate_model(model, X_test, y_test)
        save_model(model)
        # Log parameters and metrics to MLflow
        mlflow.log_param("model_type", "RandomForestRegressor")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 12)
        mlflow.log_metrics(metrics)
        # Provide input_example for model signature
        input_example = X_test.iloc[:5]
        mlflow.sklearn.log_model(model, name="model", input_example=input_example)
        # Optionally save metrics to a file
        metrics_path = MODEL_PATH / "metrics.csv"
        pd.DataFrame([metrics]).to_csv(metrics_path, index=False)
        print(f"📄 Metrics saved to {metrics_path}")

if __name__ == "__main__":
    run_pipeline()
