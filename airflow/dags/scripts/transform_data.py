from io import BytesIO
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
    chunks = pd.read_csv(
        csv_object["Body"],
        dtype=dtypes,
        chunksize=10000,  # use smaller chunks if memory issues arise
    )
    df = pd.concat(chunks, ignore_index=True)
    return df


def transform_df(df):
    # replace "Yes/No" values with True/False
    df["Tested"] = df["Tested"].replace({"Yes": True, "No": False, None: False})
    # rename "Tested" column to "DrugTested" for downstream reporting clarity
    df.rename(columns={"Tested": "DrugTested"}, inplace=True)
    return df


def write_parquet_to_s3(df, bucket, object_key):
    print(f"Writing dataframe to s3://{bucket}/{object_key}")
    with BytesIO() as bytes_io:
        df.to_parquet(bytes_io, compression="gzip")
        bytes_io.seek(0)
        s3_client = boto3.client("s3")
        s3_client.upload_fileobj(bytes_io, Bucket=bucket, Key=object_key)
    print(f"Successfully wrote to s3://{bucket}/{object_key}")
    return df


def transform_data():
    csv_object = download_latest_from_s3("openpowerlifting-data-raw")
    df = read_csv_to_df(csv_object)
    df = transform_df(df)
    write_parquet_to_s3(
        df, "openpowerlifting-data-curated", "openpowerlifting-data.parquet"
    )


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    os.getenv("AWS_ACCESS_KEY_ID")
    os.getenv("AWS_SECRET_ACCESS_KEY")

    transform_data()
