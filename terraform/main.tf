resource "google_storage_bucket" "ml_bucket" {
  name     = var.bucket_name
  location = var.gcp_region
  force_destroy = true
}

resource "google_compute_instance" "ml_vm" {
  name         = var.vm_name
  machine_type = "e2-standard-4"
  zone         = "${var.gcp_region}-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 50
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt-get update
    sudo apt-get install -y docker.io git
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
    # Optionally: pull your Docker image here
  EOT

  tags = ["ml-pipeline"]
}

resource "google_bigquery_dataset" "retail_sales" {
  dataset_id                  = "retail_sales"
  project                     = var.gcp_project
  location                    = var.gcp_region
  delete_contents_on_destroy  = true
}

resource "google_bigquery_table" "sales_clean" {
  dataset_id = google_bigquery_dataset.retail_sales.dataset_id
  table_id   = "sales_clean"
  project    = var.gcp_project

  schema = jsonencode([]) # Schema will be auto-detected by load job
}
