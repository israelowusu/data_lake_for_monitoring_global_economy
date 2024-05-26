import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage
from google.cloud import bigquery

# Replace with your project ID and bucket name
project_id = "intrepid-period-422622-n5"
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
for filename in [
    "Exports Merchandise, Customs, constant 2010 US$, millions, not seas. adj..xlsx",
    "Exports Merchandise, Customs, constant 2010 US$, millions, seas. adj..xlsx",
    "Exports Merchandise, Customs, current US$, millions, not seas. adj..xlsx",
    "Exports Merchandise, Customs, current US$, millions, seas. adj..xlsx"
]:
    extracted_data = extract_data_from_excel(filename, desired_columns.copy())
    base_name, _ = os.path.splitext(filename)  # Split filename and extension
    new_filename = f"{base_name.lower().replace(' ', '_')}_{file_count}.parquet"
    all_data_by_dataset[new_filename] = extracted_data
    file_count += 1  # Increment counter for filenames

# Convert data to Parquet for each dataset
for dataset_name, data in all_data_by_dataset.items():
    table = pa.Table.from_pylist(data)
    pq.write_table(table, dataset_name)  # Use the new filename directly

# Upload Parquet files to GCS
client = storage.Client(project=project_id)
bucket = client.bucket(bucket_name)

for dataset_name in all_data_by_dataset.keys():
    blob = bucket.blob(dataset_name)
    blob.upload_from_filename(dataset_name)

print("Data extracted, converted to Parquet with descriptive names, and uploaded to GCS!")

# BigQuery loading
client = bigquery.Client(project=project_id)
dataset_id = "global_economic_monitor"

# Define BigQuery schema
schema = [
    bigquery.SchemaField("Year", "INTEGER"),
    bigquery.SchemaField("Australia", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Germany", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("United Kingdom", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Ireland", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Israel", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Japan", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Norway", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("Singapore", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("United States", "FLOAT", mode="NULLABLE"),
]

# Load data to separate BigQuery tables for each dataset
for dataset_name, data in all_data_by_dataset.items():
    table_ref = client.dataset(dataset_id).table(dataset_name.replace(".parquet", ""))
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Overwrite existing data
    )

    uri = f'gs://{bucket_name}/{dataset_name}'
    load_job = client.load_table_from_uri(
        uri,
        table_ref,
        job_config=job_config
    )

    load_job.result()  # Wait for the job to complete

    print(f"Data from {dataset_name} loaded to BigQuery table: {dataset_id}.{dataset_name.replace('.parquet', '')}")
