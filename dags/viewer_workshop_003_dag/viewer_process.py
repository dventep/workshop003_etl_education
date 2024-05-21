import requests
import pandas as pd
import logging
import json
import sys
import os
import warnings
sys.path.append(os.path.abspath("/opt/airflow/shared_functions/"))
from connect_database import ConnectionPostgres
from kafka_functions import kafka_consumer, create_topic, delete_topic

def create_table():
    """ Create table in the database. """
    
    logging.info("Creating table")
    connection = ConnectionPostgres("/opt/airflow/config/credentials.ini")
    connection.make_tables()
    connection.close_connection()
    logging.info("Created table")
    
def consumer(columns_list):
    """ Consume data from Kafka. """
    
    delete_topic('viewer_kafka')
    create_topic('viewer_kafka')
    consumer_kafka = kafka_consumer()
    dataframe_list = list()
    viewer_dataframe = pd.DataFrame(columns = columns_list)
    start_data = False
    for message in consumer_kafka:
        if message.value == '-/Start/-':
            start_data = True
            continue
        if message.value == '-/End/-':
            break
        if start_data:
            logging.info(f"Message consumed: {message.value}")
            dataframe = pd.json_normalize(data=message.value)
            dataframe['happiness_predicted'] = 611
            viewer_dataframe.loc[len(viewer_dataframe)] = dataframe.iloc[0].to_dict()
    consumer_kafka.close()
    logging.info(f"Dataframe: {viewer_dataframe.shape}")
    logging.info(viewer_dataframe.head())
    delete_topic('viewer_kafka')

    return viewer_dataframe.to_json(orient='records')

def load(json_data, table_name):
    """ Load data to the database. """
    
    json_data = json.loads(json_data)
    dataframe = pd.json_normalize(data=json_data)

    logging.info("Starting load process")
    connection = ConnectionPostgres("/opt/airflow/config/credentials.ini")
    dataframe.to_sql(name=table_name, con=connection.engine, if_exists='replace', index=False, index_label='id')

    connection.log('Data loaded to {}: {} rows - {} columns.' .format(connection.connection_config['database'], dataframe.shape[0], dataframe.shape[1]))

    connection.close_connection()
    logging.info(f"Data loaded in: {table_name}")
