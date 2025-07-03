"""
Module: prefect_flow.py
Purpose: Orchestrate the full ML pipeline using Prefect.
"""
from prefect import flow, task
import subprocess
from pathlib import Path

@task
def clean_and_engineer():
    subprocess.run(["python3", "src/data/data_clean_join.py"], check=True)
    subprocess.run(["python3", "src/features/engineer_features.py"], check=True)

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
    clean_and_engineer()
    train()
    predict()
    report()

if __name__ == "__main__":
    retail_pipeline()
