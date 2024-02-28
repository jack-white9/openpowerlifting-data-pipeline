from io import StringIO
import pandas as pd
import boto3
from dotenv import load_dotenv
import os


def download_latest_from_s3(bucket):
    print(f"Fetching latest file from S3 bucket: {bucket}")
    s3_client = boto3.client("s3")
    objects = s3_client.list_objects_v2(Bucket=bucket)["Contents"]
    objects.sort(key=lambda o: o["LastModified"])
    latest_key = objects[-1]["Key"]
    print(f"Found latest file: {latest_key}")
    object = s3_client.get_object(Bucket=bucket, Key=latest_key)
    return object


def read_csv_to_df(csv_object):
    print("Reading CSV file into dataframe")
    csv_string = csv_object["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    return df


def write_parquet_to_s3(df, s3_url):
    print(f"Writing dataframe to {s3_url}")
    df.to_parquet(s3_url, compression="gzip")
    print(f"Successfully wrote to {s3_url}")
    return df


if __name__ == "__main__":
    load_dotenv()
    os.getenv("AWS_ACCESS_KEY_ID")
    os.getenv("AWS_SECRET_ACCESS_KEY")

    csv_object = download_latest_from_s3("openpowerlifting-data-raw")
    df = read_csv_to_df(csv_object)
    write_parquet_to_s3(
        df, "s3://openpowerlifting-data-curated/openpowerlifting-data.parquet"
    )
