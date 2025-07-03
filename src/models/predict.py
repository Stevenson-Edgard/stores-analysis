"""
Module: predict.py
Purpose: Make predictions using the trained model on new or test data.
"""
import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("models")
MODEL_FILE = MODEL_PATH / "rf_sales_model.pkl"
INPUT_FILE = Path("data/processed/future_features.csv")  # Change as needed
OUTPUT_FILE = Path("data/predictions/predictions.csv")


def load_model(path=MODEL_FILE):
    return joblib.load(path)

def load_features(path=INPUT_FILE):
    df = pd.read_csv(path)
    # Drop target and date columns if present
    drop_cols = ["Date", "Weekly_Sales", "Total_MarkDown", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
    features = [col for col in df.columns if col not in drop_cols]
    X = pd.get_dummies(df[features], drop_first=True)
    # Align columns with training features if needed
    train_features_path = Path("data/processed/train_features.csv")
    if train_features_path.exists():
        train_df = pd.read_csv(train_features_path)
        train_features = [col for col in train_df.columns if col not in drop_cols]
        X_train = pd.get_dummies(train_df[train_features], drop_first=True)
        X = X.reindex(columns=X_train.columns, fill_value=0)
    return X, df

def make_predictions(model, X):
    return model.predict(X)

def save_predictions(df, preds, path=OUTPUT_FILE):
    df = df.copy()
    df["Predicted_Weekly_Sales"] = preds
    path.parent.mkdir(exist_ok=True, parents=True)
    df.to_csv(path, index=False)
    print(f"Predictions saved to {path}")
    return df

def main():
    model = load_model()
    X, df = load_features()
    preds = make_predictions(model, X)
    df_with_preds = save_predictions(df, preds)
    # Generate future forecasts per store/department
    print("\nSample forecasts per store/department:")
    print(df_with_preds[["Store", "Dept", "Date", "Predicted_Weekly_Sales"]].groupby(["Store", "Dept"]).tail(1).head(10))

if __name__ == "__main__":
    main()
