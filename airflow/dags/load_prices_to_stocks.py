from airflow import DAG
from airflow.operators.python import PythonOperator
from utils import db, tinkoff
from airflow.utils.dates import days_ago
from datetime import timedelta
import os

DAG_ID = os.path.basename(__file__).replace('.pyc', '').replace('.py', '')
CONN_ID = 'postgres_stocks'

default_args = {
    'owner': 'airflow',
    'depends_on_path': False,
    'start_date': days_ago(1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
        dag_id=DAG_ID,
        default_args=default_args,
        schedule_interval=None,
) as dag:
    load_aapl_data = PythonOperator(
        task_id='load_aapl_data',
        python_callable=db.load_df_to_db,
        op_kwargs={
            'connector': CONN_ID,
            'df': tinkoff.get_data_by_ticker_and_period(
                'AAPL',
            ),
            'table_name': 'aapl',
        }
    )