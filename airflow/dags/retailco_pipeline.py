from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'retailco',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

HOME = "/home/adetoro"
VENV = f"{HOME}/airflow-venv/bin"
DBT  = f"{VENV}/dbt --no-populate-cache"

with DAG(
    dag_id='retailco_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
) as dag:

    extract = BashOperator(
        task_id='extract_from_erp',
        bash_command=f'{VENV}/python {HOME}/extractor/extractor.py',
    )

    load = BashOperator(
        task_id='load_to_warehouse',
        bash_command=f'{VENV}/python {HOME}/dlt_pipeline/load.py',
    )

    dbt_snapshot = BashOperator(
        task_id='dbt_snapshot',
        bash_command=f'cd {HOME}/retailco && {DBT} snapshot --profiles-dir {HOME}/.dbt',
    )

    dbt_staging = BashOperator(
        task_id='dbt_staging',
        bash_command=f'cd {HOME}/retailco && {DBT} run --select staging --profiles-dir {HOME}/.dbt',
    )

    dbt_marts = BashOperator(
        task_id='dbt_marts',
        bash_command=f'cd {HOME}/retailco && {DBT} run --select marts --profiles-dir {HOME}/.dbt',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {HOME}/retailco && {DBT} test --profiles-dir {HOME}/.dbt',
    )

    extract >> load >> dbt_snapshot >> dbt_staging >> dbt_marts >> dbt_test