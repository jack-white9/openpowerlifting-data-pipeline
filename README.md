# OpenPowerlifting Data Pipeline

A data pipeline extracting data from [Open Powerlifting](https://www.openpowerlifting.org/) records.

## Table of Contents

- [Project Overview](#project-overview)
  - [Extracting API data](#extracting-api-data)
  - [Transforming CSV data](#transforming-csv-data)
  - [Loading Parquet data](#loading-parquet-data)
  - [Analysing Parquet data with Amazon Athena](#analysing-parquet-data-with-amazon-athena)
- [Running Airflow Locally](#running-airflow-locally)
  - [Requirements](#requirements)
  - [Getting Started](#getting-started)
  - [Shutting Down](#shutting-down)
  - [Troubleshooting](#troubleshooting)

## Project Overview

This project contains a data pipeline that extracts, transforms, and loads powerlifting data into a data lake hosted on Amazon S3.

Features:

- ETL from API to curated data lake
- Containerised Airflow environment for orchestration
- Deployable data platform using Infrastructure as Code with Terraform
- Data Catalog using Glue to enable ad-hoc SQL queries on curated parquet data with Amazon Athena

### Extracting API data

Data is extracted daily from the [Open Powerlifting](https://www.openpowerlifting.org/) API and loaded into a raw S3 landing zone in CSV format. For cost-saving purposes, raw data will be retained for 10 days before automatic deletion.

### Transforming CSV data

CSV data from the raw S3 bucket is transformed with [pandas](https://pandas.pydata.org/) by modifying columns and values to improve clarity in downstream reporting.

### Loading Parquet data

Transformed data is converted into compressed Parquet format to reduce storage costs and improve read execution.

### Analysing Parquet data with Amazon Athena

Terraform will create a Glue Database by scanning the curated S3 bucket with a Glue Crawler, enabling ad-hoc SQL queries with Amazon Athena.

## Running Locally

This repository provides a Docker Compose setup for running Apache Airflow locally. It allows you to quickly set up an Airflow environment for development, testing, or demonstration purposes.

### Requirements

- Docker
- Docker Compose (V2)

### Getting Started

1. Clone this repository:

```sh
git clone git@github.com:jack-white9/openpowerlifting-data-pipeline.git
cd openpowerlifting-data-pipeline
```

2. Create the required AWS infrastructure:

```sh
cd terraform
terraform apply
```

3. Add AWS credentials to Docker environment

```sh
touch airflow/.env
echo "AWS_ACCESS_KEY_ID=<your aws access key id>" >> airflow/.env
echo "AWS_SECRET_ACCESS_KEY=<your aws secret access key>" >> airflow/.env
```

4. Start local Airflow services using Docker Compose:

```sh
cd airflow
docker compose up --build -d
```

5. Access the Airflow web interface:

Open a web browser and go to [http://localhost:8080](http://localhost:8080) to view the Airflow web UI.

### Shutting Down

To remove AWS infrastructure, use:

```sh
terraform destroy
```

To stop and remove Airflow containers, use:

```sh
docker compose down
```

### Troubleshooting

- If you encounter any issues, refer to the [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html) for troubleshooting tips and guidance.
- Check the logs of Airflow services for error messages:

```sh
docker compose logs <service_name>
```
