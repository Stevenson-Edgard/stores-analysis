# Retail Sales Forecasting ML Pipeline

A production-grade, end-to-end MLOps pipeline for retail sales forecasting using GCP, Terraform, Docker, MLflow, DVC, Prefect, and more.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Infrastructure Setup (Terraform)](#infrastructure-setup-terraform)
- [ML Pipeline & Orchestration](#ml-pipeline--orchestration)
- [Dockerization & CI/CD](#dockerization--cicd)
- [Data & Model Versioning](#data--model-versioning)
- [Usage: Step-by-Step](#usage-step-by-step)
- [Secrets & Access](#secrets--access)
- [Key Commands](#key-commands)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Project Overview
This project implements a robust, modular ML pipeline for retail sales forecasting, supporting:
- Automated ETL (extract, transform, load) to GCS and BigQuery
- Modular feature engineering, model training, prediction, and reporting
- MLflow experiment tracking, DVC data/model versioning
- Prefect orchestration for full pipeline automation
- Streamlit dashboard for interactive reporting
- Full cloud deployment with Terraform, Docker, and GitHub Actions

---

## Architecture
```
[Terraform] ---> [GCP: VM, GCS, BigQuery, IAM]
      |
      v
[GitHub Actions] --build/push--> [GCR]
      |
      v
[GitHub Actions] --ssh--> [GCP VM] --pull/run--> [Docker Container: ML Pipeline, Dashboard]
      |
      v
[Prefect Flow] --> [ETL] -> [Train] -> [Predict] -> [Report]
```

---

## Infrastructure Setup (Terraform)
All infrastructure is defined as code in the `terraform/` directory.
- **GCS Bucket**: For data and model storage
- **BigQuery Dataset/Table**: For processed data
- **Compute Engine VM**: For running the pipeline and dashboard
- **IAM Roles**: Least-privilege access for service accounts

**Key files:**
- `main.tf`, `variables.tf`, `outputs.tf`, `provider.tf`

**Provisioning:**
```sh
cd terraform
gcloud auth application-default login
terraform init
terraform apply
```

---

## ML Pipeline & Orchestration
- **ETL**: `src/etl/etl_gcs_bigquery.py` automates data cleaning, feature engineering, upload to GCS, and load to BigQuery.
- **Feature Engineering**: Modular, reusable, and tracked.
- **Model Training**: `src/models/train_model.py` with MLflow tracking.
- **Prediction**: `src/models/predict.py`
- **Reporting**: `src/reports/generate_report.py`
- **Orchestration**: `src/orchestration/prefect_flow.py` automates the full pipeline using Prefect.

---

## Dockerization & CI/CD
- **Dockerfile**: Packages the entire pipeline and dashboard.
- **docker-compose.yml**: For local multi-service development.
- **GitHub Actions**: `.github/workflows/deploy.yml` builds, pushes, and deploys the Docker image to the GCP VM.

---

## Data & Model Versioning
- **DVC**: Used for reproducible data and model versioning.
- **MLflow**: Tracks experiments, metrics, and artifacts.

---

## Usage: Step-by-Step

### 1. **Provision Infrastructure**
```sh
cd terraform
terraform apply
```

### 2. **Set Up Secrets**
- Store your GCP service account key as `GCP_SA_KEY` in GitHub secrets.
- Never commit secrets or large files to git.

### 3. **Build & Push Docker Image**
```sh
docker build -t gcr.io/<GCP_PROJECT>/retail-ml-pipeline:latest .
docker push gcr.io/<GCP_PROJECT>/retail-ml-pipeline:latest
```

### 4. **Run the Pipeline (Locally or on VM)**
```sh
python3 -m src.orchestration.prefect_flow
```

### 5. **ETL Standalone Example**
```sh
python3 -m src.etl.etl_gcs_bigquery \
  --input data/raw/kaggle_retail_data/sales.csv \
  --gcs-bucket <your-bucket> \
  --gcs-path data/clean/sales_clean.csv \
  --bq-dataset retail_sales \
  --bq-table sales_clean \
  --gcp-project <your-gcp-project>
```

### 6. **Access the Dashboard**
- Visit `http://<VM_EXTERNAL_IP>:8501` after deployment.

---

## Secrets & Access
- **Service Account**: Use a GCP service account with `roles/artifactregistry.reader`, `roles/storage.objectViewer`, and `roles/iam.serviceAccountUser`.
- **SSH Keys**: Managed by Terraform and GitHub Actions for VM access.
- **.gitignore**: Ensures secrets and large files are not committed.

---

## Key Commands
- **Terraform**: `terraform apply`, `terraform destroy`
- **DVC**: `dvc repro`, `dvc push`, `dvc pull`
- **Prefect**: `python3 -m src.orchestration.prefect_flow`
- **Docker**: `docker build`, `docker push`, `docker run`
- **MLflow**: `mlflow ui`
- **BigQuery**: Use GCP Console or `bq` CLI for queries

---

## Troubleshooting
- **Docker Pull Auth Errors**: Ensure `gcloud auth configure-docker --quiet` is run on the VM and the service account has the correct roles.
- **Terraform Permission Errors**: Use a user with Owner/IAM Admin for initial setup.
- **GitHub Actions Push Blocked**: Remove secrets/large files from git history and use `.gitignore`.

---

## Contributing
1. Fork the repo and create a feature branch.
2. Make your changes and add tests.
3. Open a pull request with a clear description.

---

**For any issues, see the code comments, or open an issue on GitHub.**