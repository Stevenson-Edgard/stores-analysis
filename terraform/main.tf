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
