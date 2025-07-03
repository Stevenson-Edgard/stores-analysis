"""
Module: engineer_features.py
Purpose: Feature engineering for retail sales modeling.
"""
import os
import pandas as pd
from typing import Optional

def load_train_ready(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=['Date'])

def add_date_parts(df: pd.DataFrame) -> pd.DataFrame:
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Week'] = df['Date'].dt.isocalendar().week
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    return df

def add_holiday_weight(df: pd.DataFrame) -> pd.DataFrame:
    # Custom weight: 5 for holidays, 1 otherwise
    df['HolidayWeight'] = df['IsHoliday'].apply(lambda x: 5 if x else 1)
    return df

def normalize_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[col + '_norm'] = (df[col] - min_val) / (max_val - min_val)
            else:
                df[col + '_norm'] = 0
    return df

def add_lag_feature(df: pd.DataFrame, group_cols: list, target_col: str, lag: int = 1) -> pd.DataFrame:
    lag_col = f'{target_col}_lag{lag}'
    df[lag_col] = df.groupby(group_cols)[target_col].shift(lag)
    return df

def engineer_features(input_path: str, output_path: str, add_lags: bool = False):
    df = load_train_ready(input_path)
    df = add_date_parts(df)
    df = add_holiday_weight(df)
    df = normalize_columns(df, ['CPI', 'Temperature', 'Fuel_Price', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'])
    if add_lags:
        df = add_lag_feature(df, group_cols=['Store', 'Dept'], target_col='Weekly_Sales', lag=1)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Feature-engineered data saved to {output_path}")

if __name__ == "__main__":
    input_path = os.path.join(os.path.dirname(__file__), '../../data/processed/train_ready.csv')
    output_path = os.path.join(os.path.dirname(__file__), '../../data/processed/train_features.csv')
    engineer_features(input_path, output_path, add_lags=True)
