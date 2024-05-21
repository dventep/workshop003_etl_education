import os
import sys
from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
sys.path.append(os.path.abspath("/opt/airflow/dags/streamer_workshop_003_dag/"))
from streamer_process import extract, transform, concatenate, transform_concatenated, data_streaming

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),  # Update the start date to today or an appropriate date
    'email': ['david.vente@uao.edu.co'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1, 
    'retry_delay': timedelta(minutes=1)
}

@dag(
    dag_id='streamer_workshop_003_dag',
    default_args=default_args,
    description='Our dag to predict!',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
)
def streamer_workshop_003_dag():

    @task
    def extract_datasets_task ():
        datasets_urls = {
            '2015': '/opt/airflow/data/2015.csv', 
            '2016': '/opt/airflow/data/2016.csv', 
            '2017': '/opt/airflow/data/2017.csv', 
            '2018': '/opt/airflow/data/2018.csv', 
            '2019': '/opt/airflow/data/2019.csv'
        }
        return extract(datasets_urls)
    @task
    def transform_datasets_task(json_data):
        column_names = []
        return transform(json_data, column_names)
    @task
    def concatenate_datasets_task(json_data):
        return concatenate(json_data)
    @task
    def transform_concatenated_dataset_task(json_data):
        return transform_concatenated(json_data)
    @task
    def data_streaming_task(json_data):
        return data_streaming(json_data)

    extract_step = extract_datasets_task()
    transform_step = transform_datasets_task(extract_step)
    concatenate_step = concatenate_datasets_task(transform_step)
    transform_concatenated_step = transform_concatenated_dataset_task(concatenate_step)
    data_streaming_step = data_streaming_task(transform_concatenated_step)
    
streamer_workshop_003_dag = streamer_workshop_003_dag()