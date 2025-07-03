output "bucket_url" {
  value = google_storage_bucket.ml_bucket.url
}

output "vm_external_ip" {
  value = google_compute_instance.ml_vm.network_interface[0].access_config[0].nat_ip
}
