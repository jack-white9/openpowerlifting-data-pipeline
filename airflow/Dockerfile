FROM apache/airflow:2.8.1-python3.11

WORKDIR /airflow

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
