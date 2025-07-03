terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
