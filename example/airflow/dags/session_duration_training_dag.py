from __future__ import annotations
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"
PYTHONPATH = f"{PROJECT_DIR}/src"


def pipeline_task(module: str, task_id: str) -> BashOperator:
    return BashOperator(
        task_id=task_id,
        bash_command=f"cd {PROJECT_DIR} && PYTHONPATH={PYTHONPATH} python -m {module}",
    )


with DAG(
    dag_id="session_duration_training_dag",
    description="Automated training pipeline for the session duration model.",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["mlops", "training", "session-duration"],
) as dag:
    generate_data = pipeline_task("session_duration_service.data", "generate_data")
    train_model = pipeline_task("session_duration_service.train", "train_model")
    evaluate_model = pipeline_task("session_duration_service.evaluate", "evaluate_model")
    promote_model = pipeline_task("session_duration_service.promote_model", "promote_model")

    generate_data >> train_model >> evaluate_model >> promote_model
