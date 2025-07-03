# src/data/extract_kaggle_data.py

import os
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/kaggle_retail_data")
PROCESSED_PATH = Path("data/processed")

# Define the files and their required columns
CSV_FILES = {
    'stores.csv': ['Store'],
    'features.csv': ['Store'],
    'sales.csv': ['Store', 'Dept', 'Weekly_Sales'],
}

def extract_raw_csv():
    # Define filenames
    raw_files = {
        "stores": "stores.csv",
        "features": "features.csv",
        "sales": "sales.csv"
    }

    # Create processed folder if needed
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    # Read and save each CSV
    for name, file in raw_files.items():
        src = RAW_PATH / file
        dst = PROCESSED_PATH / file

        df = pd.read_csv(src)
        df.to_csv(dst, index=False)
        print(f"✅ Processed {name}: {src} → {dst}")

    print("✅ All raw CSVs copied to data/processed/")

def check_required_columns(filename, required_columns):
    filepath = os.path.join(RAW_PATH, filename)
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filename}")
        return False
    try:
        df = pd.read_csv(filepath, nrows=1)  # Only read header
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"❌ {filename} is missing columns: {missing}")
            return False
        else:
            print(f"✅ {filename} contains all required columns: {required_columns}")
            return True
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return False

def main():
    print("Checking required columns in Kaggle retail data CSV files:\n")
    all_ok = True
    for fname, req_cols in CSV_FILES.items():
        ok = check_required_columns(fname, req_cols)
        all_ok = all_ok and ok
    if all_ok:
        print("\nAll files have the required columns.")
    else:
        print("\nSome files are missing required columns. Please review the output above.")

if __name__ == "__main__":
    extract_raw_csv()
    main()
