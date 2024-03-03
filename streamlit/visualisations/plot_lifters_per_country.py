import duckdb
import altair as alt
import streamlit as st


def plot_lifters_per_country():
    query = """
        select Country, count(distinct Name) as Participants
        from data
        where Country != '' and Country is not null
        group by Country
        order by Participants desc
        limit 10;
    """
    df = duckdb.sql(query).df()
    st.dataframe(
        df,
        column_order=("Country", "Participants"),
        hide_index=True,
        width=None,
        column_config={
            "Participants": st.column_config.ProgressColumn(
                "Participants",
                format="%f",
                min_value=0,
                max_value=max(df.Participants),
            ),
        },
    )
