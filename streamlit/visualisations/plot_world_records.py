import duckdb
import streamlit as st


def get_world_record(df, sex, weight_class, drug_tested, equipment):
    if sex is None or weight_class is None or drug_tested is None or equipment is None:
        return 0, 0, 0
    record = df[
        (df["Sex"] == sex)
        & (df["WeightClassKg"] == weight_class)
        & (df["DrugTested"] == drug_tested)
        & (df["Equipment"] == equipment)
    ].iloc[0]
    return record["MaxSquatKg"], record["MaxBenchKg"], record["MaxDeadliftKg"]


def plot_world_records():
    query = """
        select
            Sex,
            WeightClassKg,
            DrugTested,
            Equipment,
            max(Best3SquatKg) as MaxSquatKg,
            max(Best3BenchKg) as MaxBenchKg,
            max(Best3DeadliftKg) as MaxDeadliftKg
        from data
        group by Sex, WeightClassKg, DrugTested, Equipment;
    """
    df = duckdb.sql(query).df()

    selected_sex = None
    selected_weight_class = None
    selected_drug_tested = None
    selected_equipment = None

    col = st.columns((1, 1, 1, 1), gap="small")
    with col[0]:
        selected_sex = st.selectbox("Sex", df["Sex"].unique())
        squat, bench, deadlift = get_world_record(
            df,
            selected_sex,
            selected_weight_class,
            selected_drug_tested,
            selected_equipment,
        )
    with col[1]:
        selected_weight_class = st.selectbox(
            "Weight Class (kg)", df["WeightClassKg"].unique()
        )
        squat, bench, deadlift = get_world_record(
            df,
            selected_sex,
            selected_weight_class,
            selected_drug_tested,
            selected_equipment,
        )
    with col[2]:
        selected_drug_tested = st.selectbox("Drug Tested", df["DrugTested"].unique())
        squat, bench, deadlift = get_world_record(
            df,
            selected_sex,
            selected_weight_class,
            selected_drug_tested,
            selected_equipment,
        )
    with col[3]:
        selected_equipment = st.selectbox("Equipment", df["Equipment"].unique())
        squat, bench, deadlift = get_world_record(
            df,
            selected_sex,
            selected_weight_class,
            selected_drug_tested,
            selected_equipment,
        )

    col = st.columns((1, 1, 1), gap="medium")
    with col[0]:
        st.metric(label="Squat", value=f"{squat} kg")

    with col[1]:
        st.metric(label="Bench", value=f"{bench} kg")

    with col[2]:
        st.metric(label="Deadlift", value=f"{deadlift} kg")
