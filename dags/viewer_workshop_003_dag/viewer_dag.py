import os
import sys
from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
sys.path.append(os.path.abspath("/opt/airflow/dags/viewer_workshop_003_dag/"))
from viewer_process import create_table, consumer, load 

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
    dag_id='viewer_workshop_003_dag',
    default_args=default_args,
    description='Our dag to predict!',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
)
def viewer_workshop_003_dag():

    @task
    def create_table_task():
        create_table()
        return True
    @task
    def consumer_data_task(continue_action=False):
        if continue_action:
            columns_list = ["id", "happiness_score", "economy_per_capita", "family", "life_expectancy", "freedom", "government_corruption", "generosity", "year", "country_region", "happiness_predicted"]
            return consumer(columns_list)
    @task
    def load_data_task(json_data):
        table_name = 'happiness'
        load(json_data, table_name)

    create_table_step = create_table_task()
    consumer_step = consumer_data_task(create_table_step)
    load_step = load_data_task(consumer_step)
    

viewer_workshop_003_dag = viewer_workshop_003_dag()