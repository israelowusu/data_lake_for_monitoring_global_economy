variable "project_id" {
  description = "The ID of the project in which to provision resources."
  type        = string
}

variable "region" {
  description = "The region in which to provision resources."
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "The name of the GCS bucket."
  type        = string
}

variable "bucket_location" {
  description = "The location of the GCS bucket."
  type        = string
  default     = "US"
}

variable "dataset_id" {
  description = "The ID of the BigQuery dataset."
  type        = string
}

variable "dataset_location" {
  description = "The location of the BigQuery dataset."
  type        = string
  default     = "US"
}