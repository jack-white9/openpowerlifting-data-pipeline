# OpenPowerlifting Data Pipeline

A data pipeline extracting data from [Open Powerlifting](https://www.openpowerlifting.org/) records.

Features:

- API extraction
- Containerisation
- Orchestration

## Table of Contents

- [Running Airflow Locally](#running-airflow-locally)
  - [Requirements](#requirements)
  - [Getting Started](#getting-started)
  - [Shutting Down](#shutting-down)
  - [Troubleshooting](#troubleshooting)

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
