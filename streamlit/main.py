import duckdb
import streamlit as st
from visualisations.avg_male_totals_by_weight import get_avg_male_totals_by_weight


def instantiate_duckdb():
    # setup aws extension and credentials
    duckdb.sql("INSTALL aws;")
    duckdb.sql("LOAD aws;")
    duckdb.sql("CALL load_aws_credentials();")
    # connect to s3
    duckdb.sql("INSTALL httpfs;")
    duckdb.sql("LOAD httpfs;")
    duckdb.sql("CREATE SECRET (TYPE S3, PROVIDER CREDENTIAL_CHAIN);")


def read_parquet(parquet_file):
    return duckdb.read_parquet(parquet_file)


def instantiate_streamlit():
    st.set_page_config(layout="wide")
    st.title("Open Powerlifting Data Analysis")


if __name__ == "__main__":
    instantiate_streamlit()
    instantiate_duckdb()
    parquet_file = "s3://openpowerlifting-data-curated/openpowerlifting-data.parquet"
    data = read_parquet(parquet_file)
    st.altair_chart(get_avg_male_totals_by_weight(), use_container_width=True)
