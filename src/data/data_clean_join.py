"""
Module: data_clean_join.py
Purpose: Modular functions for cleaning, joining, and preparing Kaggle retail data for modeling.
"""
import os
import pandas as pd
from typing import Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw/kaggle_retail_data')

# 1. Load Data
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(os.path.join(DATA_DIR, 'sales.csv'))
    stores = pd.read_csv(os.path.join(DATA_DIR, 'stores.csv'))
    features = pd.read_csv(os.path.join(DATA_DIR, 'features.csv'))
    return sales, stores, features

# 2. Clean Data
def clean_sales(sales: pd.DataFrame) -> pd.DataFrame:
    sales['Date'] = pd.to_datetime(sales['Date'], dayfirst=True, errors='coerce')
    return sales

def clean_stores(stores: pd.DataFrame) -> pd.DataFrame:
    return stores

def clean_features(features: pd.DataFrame) -> pd.DataFrame:
    features['Date'] = pd.to_datetime(features['Date'], dayfirst=True, errors='coerce')
    for col in [f'MarkDown{i}' for i in range(1,6) if f'MarkDown{i}' in features.columns]:
        features[col] = features[col].fillna(0)
    return features

# 3. Join Data
def join_data(sales: pd.DataFrame, stores: pd.DataFrame, features: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(sales, features, on=['Store', 'Date', 'IsHoliday'], how='left')
    merged = pd.merge(merged, stores, on='Store', how='left')
    return merged

# 4. Save Model-Ready Data
def save_model_ready(df: pd.DataFrame, out_path: str):
    df.to_csv(out_path, index=False)

# 5. Main pipeline
def main():
    sales, stores, features = load_data()
    sales = clean_sales(sales)
    stores = clean_stores(stores)
    features = clean_features(features)
    model_ready = join_data(sales, stores, features)
    out_path = os.path.join(os.path.dirname(__file__), '../../data/processed/train_ready.csv')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    save_model_ready(model_ready, out_path)
    print(f"Model-ready data saved to {out_path}")

if __name__ == "__main__":
    main()
