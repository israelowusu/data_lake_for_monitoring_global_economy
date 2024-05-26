import os
import pandas as pd
import pyarrow as pa
from google.cloud import storage
from google.cloud import bigquery

# Replace with your project ID and bucket name
project_id = "your-project-id"
bucket_name = "global-economic-monitor"


def extract_data_from_excel(filename, desired_columns):
  df = pd.read_excel(filename)

  # Select desired columns and potentially filter by year
  data = df[desired_columns]
  
  return data.to_dict(orient='records')


# Define desired columns (including 'Year')
desired_columns = ["Year", "Australia", "Germany", "United Kingdom", "Ireland", "Israel", "Japan", "Norway", "Singapore", "United States"]

# Extract data from each Excel file and create descriptive Parquet filenames
all_data_by_dataset = {}
file_count = 1
for filename in ["Exports Merchandise, Customs, constant 2010 US$, millions, not seas. adj..xlsx",
                 "Exports Merchandise, Customs, constant 2010 US$, millions, seas. adj..xlsx",
                 "Exports Merchandise, Customs, current US$, millions, not seas. adj..xlsx",
                 "Exports Merchandise, Customs, current US$, millions, seas. adj..xlsx"]:
  extracted_data = extract_data_from_excel(filename, desired_columns.copy())
  base_name, extension = os.path.splitext(filename)  # Split filename and extension
  new_filename = f"{base_name.lower().replace(' ', '_')}_{file_count}{extension}"
  all_data_by_dataset[new_filename] = extracted_data
  file_count += 1  # Increment counter for filenames

# Convert data to Parquet for each dataset
for dataset_name, data in all_data_by_dataset.items():
  table = pa.Table.from_pydict(data)
  table.write_parquet(dataset_name)  # Use the new filename directly

# Upload Parquet files to GCS
client = storage.Client(project=project_id)
bucket = client.bucket(bucket_name)

for dataset_name in all_data_by_dataset.keys():
  blob = bucket.blob(dataset_name)
  blob.upload_from_filename(dataset_name)

print(f"Data extracted, converted to Parquet with descriptive names, and uploaded to GCS!")

# BigQuery loading
client = bigquery.Client(project=project_id)
dataset_id = "global_economic_monitor"

# Define BigQuery schema
schema = [
    pa.Field("Year", pa.Int64Type()),
    pa.Field("Australia", pa.Float64Type(), nullable=True),
    pa.Field("Germany", pa.Float64Type(), nullable=True),
    pa.Field("United Kingdom", pa.Float64Type(), nullable=True),
    pa.Field("Ireland", pa.Float64Type(), nullable=True),
    pa.Field("Israel", pa.Float64Type(), nullable=True),
    pa.Field("Japan", pa.Float64Type(), nullable=True),
    pa.Field("Norway", pa.Float64Type(), nullable=True),
    pa.Field("Singapore", pa.Float64Type(), nullable=True),
    pa.Field("United States", pa.Float64Type(), nullable=True),
]

# Load data to separate BigQuery tables for each dataset
for dataset_name, data in all_data_by_dataset.items():
  table_ref = client.dataset(dataset_id).table(f"{dataset_name}")

  job_config = bigquery.LoadJobConfig(
      schema=schema,
      write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Overwrite existing data
  )

  load_job = client.load_table_from_uri(
    f'gs://{bucket_name}/{dataset_name}.parquet',
    table_ref,
    job_config=job_config
  )

  load_job.result()  # Wait for the job to complete

  print(f"Data from {dataset_name} loaded to BigQuery table: {dataset_id}.{dataset_name}")
