"""
Module: visualize_shap.py
Purpose: Visualize SHAP feature importances for the trained Random Forest model.
"""
import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
from pathlib import Path

MODEL_PATH = Path("models")
MODEL_FILE = MODEL_PATH / "rf_sales_model.pkl"
FEATURES_FILE = Path("data/processed/train_features.csv")


def load_model(path=MODEL_FILE):
    return joblib.load(path)

def load_features(path=FEATURES_FILE):
    df = pd.read_csv(path)
    # Drop target and date columns
    drop_cols = ["Date", "Weekly_Sales", "Total_MarkDown", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]
    features = [col for col in df.columns if col not in drop_cols]
    X = pd.get_dummies(df[features], drop_first=True)
    return X

def plot_shap_summary(model, X):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig(MODEL_PATH / "shap_summary.png")
    print(f"SHAP summary plot saved to {MODEL_PATH / 'shap_summary.png'}")

def main():
    model = load_model()
    X = load_features()
    plot_shap_summary(model, X)

if __name__ == "__main__":
    main()
