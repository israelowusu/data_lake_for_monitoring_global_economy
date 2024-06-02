***Global Economic Monitor Data Lake***

This project is designed to create a data lake architecture for monitoring global economic data using World Bank open data. 
The project involves extracting data from Excel files, transforming and storing it in Google Cloud Storage, 
loading it into BigQuery for further processing, and visualizing the data using Grafana. Prefect is used for orchestrating the data pipeline.


**Table of Contents**

    1. Architecture
    2. Setup and Installation
    3. Project Structure
    4. Data Pipeline
    5. Running the Pipeline
    6. Visualization
    7. License

**Architecture**

The data pipeline architecture is as follows:

  1. Excel: Read data from Excel files.
  2. Python: Use Python scripts to read data and convert it into Parquet format.
  3. Cloud Storage: Store the Parquet files in Google Cloud Storage.
  4. BigQuery: Load and transform data in BigQuery.
  5. Grafana: Visualize the processed data.
  6. Prefect: Orchestrate the entire pipeline.

![image](https://github.com/israelowusu/data_lake_for_monitoring_global_economy/assets/92272985/0e715373-cac0-4817-ac92-0d795a1b1e7e)



**Setup and Installation**

Prerequisites

  1. Python 3.7 or higher
  2. Google Cloud account with BigQuery and Cloud Storage enabled
  3. Prefect
  4. Grafana

Installation

  1. Clone the repository:

    git clone https://github.com/israelowusu/data_lake_for_monitoring_global_economy.git
    cd data_lake_for_monitoring_global_economy

  2. Create a virtual environment and activate it:

    python3 -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`

  3. Install the required packages:

    pip install -r requirements.txt

  4. Set up Google Cloud credentials:

    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"

**Project Structure**

  1. bigquery_transformed_data/: Contains the transformed data loaded into BigQuery.
  2. dashboards/: Contains Grafana dashboards for visualizing the data.
  3. data/: Raw data files and intermediate data.
  4. terraform/: Terraform scripts for provisioning Google Cloud resources.
  5. .gitignore: Specifies files and directories to be ignored by Git.
  6. DataLakePipeline_Architecture.jpg: Diagram of the data pipeline architecture.
  7. LICENSE: License for the project.
  8. data_pipeline.py: Prefect flow script for the data pipeline.
  9. main.py: Script to execute the data pipeline.
  10. prefect_flowrun.png: Image showing the Prefect flow run.
  11. requirements.txt: Python dependencies.


**Data Pipeline**

Extraction

  The data is extracted from Excel files using Python's pandas library.

Transformation

  The extracted data is transformed into Parquet format and stored in Google Cloud Storage.

Loading

  The Parquet files are loaded into BigQuery where further transformations are performed.

Visualization

  The processed data is visualized using Grafana.


**Running the Pipeline**

  1. Ensure all dependencies are installed and Google Cloud credentials are set up.

  2. Execute the pipeline using Prefect:

    prefect run -p main.py

  3. The pipeline will read data from Excel files, transform and load it into BigQuery, and make it available for visualization in Grafana.


**Visualization**

Grafana is used to create interactive dashboards to visualize the data stored in BigQuery. To set up Grafana:

  1. Install Grafana and the BigQuery plugin.
  2. Connect Grafana to BigQuery using your Google Cloud credentials.
  3. Import the dashboards from the dashboards directory.

**License**

This project is licensed under the MIT License - see the LICENSE file for details.
