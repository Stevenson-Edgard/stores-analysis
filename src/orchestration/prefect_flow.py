"""
Module: prefect_flow.py
Purpose: Orchestrate the full ML pipeline using Prefect.
"""
from prefect import flow, task
import subprocess
from pathlib import Path

@task
def etl_to_gcs_bigquery():
    subprocess.run([
        "python3", "-m", "src.etl.etl_gcs_bigquery",
        "--input", "data/raw/kaggle_retail_data/sales.csv",
        "--gcs-bucket", "stores-analysis-464721-stevenson-20250630",
        "--gcs-path", "data/clean/sales_clean.csv",
        "--bq-dataset", "retail_sales",
        "--bq-table", "sales_clean",
        "--gcp-project", "stores-analysis-464721"
    ], check=True)

@task
def train():
    subprocess.run(["python3", "src/models/train_model.py"], check=True)

@task
def predict():
    subprocess.run(["python3", "src/features/generate_future_features.py"], check=True)
    subprocess.run(["python3", "src/models/predict.py"], check=True)

@task
def report():
    subprocess.run(["python3", "src/reports/generate_report.py"], check=True)

@flow(name="Retail ML Pipeline")
def retail_pipeline():
    etl_to_gcs_bigquery()
    train()
    predict()
    report()

if __name__ == "__main__":
    retail_pipeline()
