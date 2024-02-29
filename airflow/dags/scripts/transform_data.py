from io import StringIO
import pandas as pd
import boto3


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
    # define dtypes to optimise pandas memory consumption
    dtypes = {
        "Name": "object",
        "Sex": "object",
        "Event": "object",
        "Equipment": "object",
        "Age": "float64",
        "AgeClass": "object",
        "BirthYearClass": "object",
        "Division": "object",
        "BodyweightKg": "float64",
        "WeightClassKg": "object",
        "Squat1Kg": "float64",
        "Squat2Kg": "float64",
        "Squat3Kg": "float64",
        "Squat4Kg": "float64",
        "Best3SquatKg": "float64",
        "Bench1Kg": "float64",
        "Bench2Kg": "float64",
        "Bench3Kg": "float64",
        "Bench4Kg": "float64",
        "Best3BenchKg": "float64",
        "Deadlift1Kg": "float64",
        "Deadlift2Kg": "float64",
        "Deadlift3Kg": "float64",
        "Deadlift4Kg": "float64",
        "Best3DeadliftKg": "float64",
        "TotalKg": "float64",
        "Place": "object",
        "Dots": "float64",
        "Wilks": "float64",
        "Glossbrenner": "float64",
        "Goodlift": "float64",
        "Tested": "object",
        "Country": "object",
        "State": "object",
        "Federation": "object",
        "ParentFederation": "object",
        "Date": "object",
        "MeetCountry": "object",
        "MeetState": "object",
        "MeetTown": "object",
        "MeetName": "object",
    }
    print("Reading CSV file into dataframe")
    csv_string = csv_object["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_string), dtype=dtypes)
    return df


def transform_df(df):
    return df


def write_parquet_to_s3(df, s3_url):
    print(f"Writing dataframe to {s3_url}")
    df.to_parquet(s3_url, compression="gzip")
    print(f"Successfully wrote to {s3_url}")
    return df


def transform_data():
    csv_object = download_latest_from_s3("openpowerlifting-data-raw")
    df = read_csv_to_df(csv_object)
    df = transform_df(df)
    write_parquet_to_s3(
        df, "s3://openpowerlifting-data-curated/openpowerlifting-data.parquet"
    )


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    os.getenv("AWS_ACCESS_KEY_ID")
    os.getenv("AWS_SECRET_ACCESS_KEY")

    transform_data()
