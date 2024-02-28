TODO:

- [x] Build custom image to install Airflow requirements
- [x] Fix blocked outbound HTTP request in DAG
- [x] Delete CSV files in S3 after 30 days
- [ ] Transform data using pandas + PythonOperator and store as Parquet in curated S3 bucket
  - [ ] (Add pandas as dependency in `requirements.txt`)
- [ ] Use Athena to query parquet data

Nice to haves:

- [ ] Logging (CloudWatch)
- [ ] Tests
