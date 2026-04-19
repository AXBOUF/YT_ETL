FROM apache/airflow:slim-3.2.1rc2-python3.14

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt