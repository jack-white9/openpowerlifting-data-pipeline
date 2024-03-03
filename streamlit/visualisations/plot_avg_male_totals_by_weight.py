import duckdb
import altair as alt
import streamlit as st


def plot_avg_male_totals_by_weight():
    weight_class_query = """
        SELECT WeightClassKg, AVG(TotalKg) AS AverageTotalKg
        FROM data WHERE ParentFederation = 'IPF' AND Sex = 'M' AND EXTRACT('year' FROM date::DATE) > 2020
        GROUP BY WeightClassKg
        ORDER BY LEN(WeightClassKg), WeightClassKg;
    """
    weight_class_male_df = duckdb.sql(weight_class_query).df()
    st.altair_chart(
        alt.Chart(weight_class_male_df)
        .mark_bar()
        .encode(
            x=alt.X("WeightClassKg", title="Weight class (kg)", sort=None),
            y=alt.Y("AverageTotalKg", title="Average total (kg)"),
        ),
        use_container_width=True,
    )
