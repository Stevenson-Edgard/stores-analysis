"""
ETL script: Extract, Transform, Load data to GCS and BigQuery
- Extracts raw data (local or remote)
- Cleans/transforms using existing modules
- Uploads processed data to GCS
- Loads data from GCS to BigQuery

Usage:
    python etl_gcs_bigquery.py --input data/raw/sales.csv --gcs-bucket my-bucket --gcs-path data/clean/sales_clean.csv --bq-dataset my_dataset --bq-table sales_clean

Requires:
    - google-cloud-storage
    - google-cloud-bigquery
    - pandas
    - Existing cleaning/feature modules
"""
import argparse
import os
import pandas as pd
from google.cloud import storage, bigquery
from src.data.data_clean_join import clean_sales, clean_stores, clean_features, join_data
from src.features.engineer_features import engineer_features  # adjust as needed

def upload_to_gcs(local_path, bucket_name, gcs_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"Uploaded {local_path} to gs://{bucket_name}/{gcs_path}")

def load_to_bigquery(gcs_uri, dataset_id, table_id, project=None):
    client = bigquery.Client(project=project)
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    load_job = client.load_table_from_uri(
        gcs_uri, table_ref, job_config=job_config
    )
    load_job.result()
    print(f"Loaded data into BigQuery: {dataset_id}.{table_id}")

def main(args):
    # 1. Extract sales (from input), stores and features (from default locations)
    print(f"Reading sales data from {args.input}")
    sales = pd.read_csv("data/raw/kaggle_retail_data/sales.csv")
    stores = pd.read_csv("data/raw/kaggle_retail_data/stores.csv")
    features = pd.read_csv("data/raw/kaggle_retail_data/features.csv")

    # 2. Clean
    sales = clean_sales(sales)
    stores = clean_stores(stores)
    features = clean_features(features)

    # 3. Join
    df_clean = join_data(sales, stores, features)

    # 4. Save cleaned data to data/processed
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)
    clean_path = os.path.join(processed_dir, "cleaned_data.csv")
    df_clean.to_csv(clean_path, index=False)

    # 5. Feature engineering using file paths
    feat_path = os.path.join(processed_dir, "feature_engineered.csv")
    engineer_features(clean_path, feat_path)
    df_feat = pd.read_csv(feat_path)

    # 6. Upload to GCS
    upload_to_gcs(feat_path, args.gcs_bucket, args.gcs_path)
    gcs_uri = f"gs://{args.gcs_bucket}/{args.gcs_path}"

    # 7. Load to BigQuery
    load_to_bigquery(gcs_uri, args.bq_dataset, args.bq_table, args.gcp_project)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL to GCS and BigQuery")
    parser.add_argument("--input", required=True, help="Path to raw sales CSV")
    parser.add_argument("--gcs-bucket", required=True, help="GCS bucket name")
    parser.add_argument("--gcs-path", required=True, help="GCS object path for cleaned data")
    parser.add_argument("--bq-dataset", required=True, help="BigQuery dataset name")
    parser.add_argument("--bq-table", required=True, help="BigQuery table name")
    parser.add_argument("--gcp-project", required=False, help="GCP project ID (optional)")
    args = parser.parse_args()
    main(args)
