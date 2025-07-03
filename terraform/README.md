# Terraform GCP Infrastructure for Retail ML Pipeline

## Usage

1. Authenticate with GCP:
   ```sh
   gcloud auth application-default login
   ```
2. Initialize Terraform:
   ```sh
   cd terraform
   terraform init
   ```
3. Apply with defaults (project and bucket pre-filled):
   ```sh
   terraform apply
   ```
   Or override any variable:
   ```sh
   terraform apply -var="gcp_project=your-gcp-project" -var="bucket_name=your-ml-bucket"
   ```

## Resources Created
- Google Cloud Storage bucket for data/models
- Compute Engine VM for running pipeline/dashboard

## Next Steps
- SSH into the VM and run your Docker containers
- Use the bucket for DVC/MLflow remote storage
