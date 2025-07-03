"""
Streamlit Dashboard for Retail Sales Forecasting
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

# Paths
METRICS_PATH = Path("models/metrics.csv")
PREDICTIONS_PATH = Path("data/predictions/predictions.csv")
SHAP_PLOT_PATH = Path("models/shap_summary.png")

st.set_page_config(page_title="Retail Sales Forecast Dashboard", layout="wide")
st.title("🏪 Retail Sales Forecast Dashboard")

# Metrics
st.header("Model Metrics")
if METRICS_PATH.exists():
    metrics = pd.read_csv(METRICS_PATH)
    st.dataframe(metrics)
else:
    st.warning("Metrics file not found.")

# SHAP Feature Importance
st.header("Feature Importance (SHAP)")
if SHAP_PLOT_PATH.exists():
    st.image(str(SHAP_PLOT_PATH), caption="SHAP Summary Plot", use_column_width=True)
else:
    st.warning("SHAP summary plot not found.")

# Predictions
st.header("Predictions Explorer")
if PREDICTIONS_PATH.exists():
    preds = pd.read_csv(PREDICTIONS_PATH)
    preds["Date"] = pd.to_datetime(preds["Date"])
    st.dataframe(preds.head(20))
    # Multi-select for stores and departments
    stores = st.multiselect("Select Store(s):", sorted(preds["Store"].unique()), default=sorted(preds["Store"].unique())[:1])
    depts = st.multiselect("Select Department(s):", sorted(preds["Dept"].unique()), default=sorted(preds["Dept"].unique())[:1])
    date_range = st.date_input("Select Date Range:", [preds["Date"].min(), preds["Date"].max()])
    filtered = preds[
        preds["Store"].isin(stores) &
        preds["Dept"].isin(depts) &
        (preds["Date"] >= pd.to_datetime(date_range[0])) &
        (preds["Date"] <= pd.to_datetime(date_range[1]))
    ]
    st.subheader("Predicted Weekly Sales Over Time")
    if "Actual_Weekly_Sales" in filtered.columns:
        st.line_chart(
            filtered.set_index("Date")[["Actual_Weekly_Sales", "Predicted_Weekly_Sales"]],
            use_container_width=True
        )
        st.subheader("Actual vs. Predicted Scatter Plot")
        st.scatter_chart(filtered[["Actual_Weekly_Sales", "Predicted_Weekly_Sales"]])
    else:
        st.line_chart(filtered.set_index("Date")["Predicted_Weekly_Sales"])
    st.subheader("Distribution of Predicted Sales")
    st.bar_chart(filtered["Predicted_Weekly_Sales"])
    # Download option
    st.download_button("Download Filtered Predictions as CSV", filtered.to_csv(index=False), "filtered_predictions.csv")
else:
    st.warning("Predictions file not found.")

st.markdown("---")
st.markdown("Created with Streamlit | Powered by your ML pipeline 🚀")
