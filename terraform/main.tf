provider "google" {
  project = var.project_id
  region  = var.region
}

# Google Cloud Storage bucket
resource "google_storage_bucket" "my_bucket" {
  name          = var.bucket_name
  location      = var.bucket_location
  force_destroy = true  # This is optional. Use it with caution.

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }
}

# BigQuery dataset
resource "google_bigquery_dataset" "my_dataset" {
  dataset_id = var.dataset_id
  location   = var.dataset_location
}

# Output the bucket URL
output "bucket_url" {
  value = google_storage_bucket.my_bucket.url
}

# Output the BigQuery dataset ID
output "bigquery_dataset_id" {
  value = google_bigquery_dataset.my_dataset.dataset_id
}
