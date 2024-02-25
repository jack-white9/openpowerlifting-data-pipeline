from io import BytesIO
import requests
import zipfile
import boto3
from botocore.exceptions import ClientError
from datetime import datetime


def get_data(url):
    try:
        print(f"Fetching data from {url}")
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException as e:
        raise e


def unzip_file(zip_file):
    zip_content = BytesIO(zip_file.content)
    with zipfile.ZipFile(zip_content, "r") as zip_file:
        print("Unzipping file contents")
        csv_file = [
            file for file in zip_file.namelist() if file.lower().endswith(".csv")
        ][0]
        return csv_file


def upload_to_s3(file, bucket, object_key):
    s3_client = boto3.client("s3")
    formatted_datetime = datetime.now().strftime("%Y-%m-%d")
    try:
        print(f"Uploading {file} to S3 bucket {bucket}")
        s3_client.put_object(
            Body=file, Bucket=bucket, Key=f"{formatted_datetime}-{object_key}"
        )
        print(f"{file} successfully uploaded to {bucket}")
    except ClientError as e:
        raise e


def extract_data():
    url = "https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip"
    zip_file = get_data(url)
    csv_file = unzip_file(zip_file)
    upload_to_s3(
        csv_file,
        "openpowerlifting-data-bronze",
        "openpowerlifting-data",
    )


if __name__ == "__main__":
    extract_data()
