from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess
import os

DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

DAG_NAME = 'retrain_model'

# Проверка дрифта с помощью Evidently
def check_drift_and_retrain():
    subprocess.run([
        "python", "-m", "src.monitoring.drift_monitor"
    ], check=True)

    # Если отчет HTML содержит "Drift detected", запускаем обучение
    if os.path.exists("reports/drift_report.html"):
        with open("reports/drift_report.html") as f:
            report_content = f.read()
        if "Drift detected" in report_content:
            print("Drift detected, starting model retraining")
            subprocess.run([
                "python", "-m", "src.create_models.train"
            ], check=True)
        else:
            print("No significant drift detected, skipping retraining.")

with DAG(
    DAG_NAME,
    default_args=DEFAULT_ARGS,
    description='Retrain model DAG triggered by drift or schedule',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    retrain_task = PythonOperator(
        task_id='check_drift_and_retrain',
        python_callable=check_drift_and_retrain
    )
