output "bucket_url" {
  value = google_storage_bucket.ml_bucket.url
}

output "vm_external_ip" {
  value = google_compute_instance.ml_vm.network_interface[0].access_config[0].nat_ip
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.retail_sales.dataset_id
}

output "bigquery_table_id" {
  value = google_bigquery_table.sales_clean.table_id
}
