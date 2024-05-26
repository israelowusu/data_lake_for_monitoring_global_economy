# Create a Cloud Storage bucket for data storage
resource "google_storage_bucket" "data_bucket" {
  name          = "global-economic-monitor"
  location     = google.region.self  # Inherits region from provider
  force_destroy = true  # Optional: Allows destroying bucket with contents
}


# Create a BigQuery dataset for data storage and analysis
resource "google_bigquery_dataset" "data_set" {
  dataset_id = "global_economic_monitor"
}
