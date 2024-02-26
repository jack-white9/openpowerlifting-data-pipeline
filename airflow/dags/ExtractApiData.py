from airflow.decorators import dag, task
from pendulum import yesterday, duration
from scripts.extract_data import extract_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": duration(minutes=1),
}


@dag(
    start_date=yesterday(),
    schedule="@daily",
    default_args=default_args,
)
def extract_api_data():
    @task(task_id="extract_data")
    def extract_data_task():
        extract_data()
        return "Extracted data successfully"

    extract_data_task()


extract_api_data()
