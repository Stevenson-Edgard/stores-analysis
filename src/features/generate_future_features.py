"""
Module: generate_future_features.py
Purpose: Generate a future-dated feature set for forecasting with the trained model.
"""
import pandas as pd
from pathlib import Path
from datetime import timedelta

# Config
N_WEEKS = 12  # Number of weeks to forecast
TRAIN_FEATURES_PATH = Path("data/processed/train_features.csv")
OUTPUT_PATH = Path("data/processed/future_features.csv")


def get_latest_data():
    df = pd.read_csv(TRAIN_FEATURES_PATH, parse_dates=["Date"])
    latest_date = df["Date"].max()
    # Use the last available week for each Store/Dept as a template
    latest = df.sort_values("Date").groupby(["Store", "Dept"]).tail(1)
    return latest, latest_date

def generate_future_dates(start_date, n_weeks):
    return [start_date + timedelta(weeks=i) for i in range(1, n_weeks + 1)]

def generate_future_features():
    latest, last_date = get_latest_data()
    future_dates = generate_future_dates(last_date, N_WEEKS)
    rows = []
    for _, row in latest.iterrows():
        for date in future_dates:
            new_row = row.copy()
            new_row["Date"] = date
            new_row["Year"] = date.year
            new_row["Month"] = date.month
            new_row["Week"] = date.isocalendar().week
            new_row["DayOfWeek"] = date.weekday()
            # Set IsHoliday, MarkDowns, etc. to 0 (or estimate as needed)
            if "IsHoliday" in new_row: new_row["IsHoliday"] = 0
            for i in range(1, 6):
                col = f"MarkDown{i}"
                if col in new_row: new_row[col] = 0
            rows.append(new_row)
    future_df = pd.DataFrame(rows)
    OUTPUT_PATH.parent.mkdir(exist_ok=True, parents=True)
    future_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Future feature set saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_future_features()
