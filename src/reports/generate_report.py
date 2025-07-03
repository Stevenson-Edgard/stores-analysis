"""
Module: generate_report.py
Purpose: Auto-generate a markdown report with metrics, feature importances, and sample predictions.
"""
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("models")
METRICS_FILE = MODEL_PATH / "metrics.csv"
SHAP_PLOT = MODEL_PATH / "shap_summary.png"
PREDICTIONS_FILE = Path("data/predictions/predictions.csv")
REPORT_FILE = Path("reports/model_report.md")


def load_metrics(path=METRICS_FILE):
    return pd.read_csv(path)

def load_predictions(path=PREDICTIONS_FILE, n=5):
    df = pd.read_csv(path)
    return df.head(n)

def generate_report():
    metrics = load_metrics()
    preds = load_predictions()
    with open(REPORT_FILE, "w") as f:
        f.write("# Model Report\n\n")
        f.write("## Metrics\n\n")
        f.write("```")
        f.write("\n" + metrics.to_markdown(index=False) + "\n")
        f.write("```\n")
        f.write("\n---\n\n")
        f.write("## SHAP Feature Importance\n\n")
        f.write(f"![SHAP Summary Plot]({SHAP_PLOT})\n\n")
        f.write("---\n\n")
        f.write("## Sample Predictions\n\n")
        f.write("```")
        f.write("\n" + preds.to_markdown(index=False) + "\n")
        f.write("```\n")
    print(f"Report generated at {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
