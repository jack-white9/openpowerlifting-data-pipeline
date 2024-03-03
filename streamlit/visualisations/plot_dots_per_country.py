import duckdb
import streamlit as st
import plotly.express as px
import country_converter as coco


def plot_dots_per_country():
    query = """
        select Country, avg(Dots) as AverageDots
        from data
        where Country != '' and Country is not null
        group by Country
    """
    df = duckdb.sql(query).df()

    cc = coco.CountryConverter()
    df.insert(0, "IsoCountry", cc.convert(names=df.Country, src="regex", to="ISO3"))

    choropleth = px.choropleth(
        df,
        locations="IsoCountry",
        color="AverageDots",
        color_continuous_scale="blues",  # greens
        range_color=(0, max(df.AverageDots)),
        labels={"AverageDots": "Average Dots", "Country": "Country"},
    )
    choropleth.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
    )

    st.plotly_chart(choropleth, use_container_width=True)
