from io import StringIO
import pandas as pd
import boto3
from dotenv import load_dotenv
import os


def download_from_s3(bucket, object_key):
    print(f"Fetching {object_key} from S3 bucket: {bucket}")
    s3_client = boto3.client("s3")
    object = s3_client.get_object(Bucket=bucket, Key=object_key)
    return object


def read_csv_to_df(csv_object):
    print("Reading CSV file into dataframe")
    csv_string = csv_object["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_string))
    return df


def write_parquet_to_s3(df, s3_url):
    print(f"Writing dataframe to {s3_url}")
    df.to_parquet(s3_url, compression="gzip")
    return df


if __name__ == "__main__":
    load_dotenv()
    os.getenv("AWS_ACCESS_KEY_ID")
    os.getenv("AWS_SECRET_ACCESS_KEY")

    csv_object = download_from_s3(
        "openpowerlifting-data-raw", "2024-02-28-openpowerlifting-data.csv"
    )
    df = read_csv_to_df(csv_object)
    write_parquet_to_s3(
        df, "s3://openpowerlifting-data-curated/openpowerlifting-data.parquet"
    )
