import duckdb
import streamlit as st
import altair as alt
from visualisations.plot_dots_per_country import plot_dots_per_country
from visualisations.plot_avg_male_totals_by_weight import plot_avg_male_totals_by_weight
from visualisations.plot_avg_female_totals_by_weight import (
    plot_avg_female_totals_by_weight,
)
from visualisations.plot_lifters_per_country import plot_lifters_per_country


def init_duckdb():
    # setup aws extension and credentials
    duckdb.sql("INSTALL aws;")
    duckdb.sql("LOAD aws;")
    duckdb.sql("CALL load_aws_credentials();")
    # connect to s3
    duckdb.sql("INSTALL httpfs;")
    duckdb.sql("LOAD httpfs;")
    duckdb.sql("CREATE OR REPLACE SECRET (TYPE S3, PROVIDER CREDENTIAL_CHAIN);")


def read_parquet(parquet_file):
    return duckdb.read_parquet(parquet_file)


def init_streamlit():
    st.set_page_config(
        page_title="OpenPowerlifting Dashboard",
        page_icon="🏋️‍♂️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    alt.themes.enable("dark")
    st.title("Open Powerlifting Data Analysis")

    col = st.columns((2, 4.5, 1.5), gap="medium")

    with col[0]:
        st.markdown("#### Average Totals by Weight Class")
        st.markdown("##### Male")
        plot_avg_male_totals_by_weight()
        st.markdown("##### Female")
        plot_avg_female_totals_by_weight()

    with col[1]:
        st.markdown("#### Average Dots per Country")
        plot_dots_per_country()

        st.markdown("#### World Records")

    with col[2]:
        st.markdown("#### Top Countries")
        plot_lifters_per_country()

        with st.expander("About", expanded=True):
            st.write(
                """
                - :orange[**Data**]: [OpenPowerlifting.org](<https://openpowerlifting.gitlab.io/opl-csv/>).
                - :orange[**Dots**]: A formula that takes into account an athlete's body weight, the weight they lifted, and the world record for their weight class in the lift they performed.
                """
            )


if __name__ == "__main__":
    init_duckdb()
    parquet_file = "s3://openpowerlifting-data-curated/openpowerlifting-data.parquet"
    data = read_parquet(parquet_file)
    init_streamlit()
