from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'Mikiyas',
    'start_date': datetime(2023, 12, 20),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_loading_dag',
    default_args=default_args,
    description='A DAG to load CSV data into the postgre database',
    schedule_interval='@daily',
)

load_prod_task = BashOperator(
    task_id='data_loading_prod',
    bash_command='python /path/to/your/main/project/script/load_data_prod.py',
    dag=dag,
)

load_dev_task = BashOperator(
    task_id='data_loading_dev',
    bash_command='python /path/to/your/main/project/script/load_data_dev.py',
    dag=dag,
)

load_staging_task = BashOperator(
    task_id='data_loading_staging',
    bash_command='python /path/to/your/main/project/script/load_data_staging.py',
    dag=dag,
)

load_prod_task >> load_dev_task
load_prod_task >> load_staging_task