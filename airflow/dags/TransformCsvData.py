from airflow.decorators import dag, task
from pendulum import yesterday
from scripts.transform_data import transform_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 0,
}


@dag(
    start_date=yesterday(),
    schedule="@daily",
    default_args=default_args,
)
def transform_csv_data():
    @task(task_id="transform_data")
    def transform_csv_data_task():
        transform_data()
        return "Transformed data successfully"

    transform_csv_data_task()


transform_csv_data()
