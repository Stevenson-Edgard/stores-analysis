variable "gcp_project" {
  description = "GCP project ID"
  type        = string
  default     = "stores-analysis-464721"
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Name for the GCS bucket"
  type        = string
  default     = "stores-analysis-464721-stevenson-20250630"
}

variable "vm_name" {
  description = "Name for the Compute Engine VM"
  type        = string
  default     = "ml-pipeline-vm"
}
