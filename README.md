python3 src/etl/etl_gcs_bigquery.py \
  --input data/raw/sales.csv \
  --gcs-bucket stores-analysis-464721-stevenson-20250630 \
  --gcs-path data/clean/sales_clean.csv \
  --bq-dataset retail_sales \
  --bq-table sales_clean \
  --gcp-project stores-analysis-464721