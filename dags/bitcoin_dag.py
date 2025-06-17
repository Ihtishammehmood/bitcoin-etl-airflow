from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
from dags.bitcoin_etl_tasks import extract_bitcoin_data, transform_and_load_bitcoin_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'btc_etl_pipeline',
    default_args=default_args,
    description='A DAG to fetch Bitcoin data, add technical indicators, and store in PostgreSQL.',
    schedule='@daily',
    catchup=False,
    tags=['crypto', 'etl', 'finance'],
) as dag:

    create_postgres_table = SQLExecuteQueryOperator(
        task_id='create_postgres_table',
        conn_id='postgres_default',
        sql="""
            CREATE TABLE IF NOT EXISTS bitcoin_metrics (
                date DATE PRIMARY KEY,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                adj_close NUMERIC,
                volume BIGINT,
                sma_20 NUMERIC,
                ema_50 NUMERIC,
                rsi_14 NUMERIC,
                macd_12_26_9 NUMERIC,
                macdh_12_26_9 NUMERIC,
                macds_12_26_9 NUMERIC
            );
            TRUNCATE TABLE bitcoin_metrics;
        """,
    )

    extract_data = PythonOperator(
        task_id='extract_bitcoin_data',
        python_callable=extract_bitcoin_data,
    )

    transform_and_load_data = PythonOperator(
        task_id='transform_and_load_bitcoin_data',
        python_callable=transform_and_load_bitcoin_data,
    )

    create_postgres_table >> extract_data >> transform_and_load_data