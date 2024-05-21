import requests
import pandas as pd
import logging
import json
import sys
import os
import warnings
sys.path.append(os.path.abspath("/opt/airflow/shared_functions/"))
from apply_columns import get_columns, get_region_by_country
from kafka_functions import kafka_producer


def extract(datasets_urls):
    """ Extract the data from the datasets. """
    logging.info("Starting data extraction")

    datasets_dict = dict()
    for (year, url) in datasets_urls.items():
        dataset = pd.read_csv(url, header=0, delimiter=',')
        datasets_dict[year] = dataset.to_dict(orient='records')
        logging.debug('Data extracted has ', dataset.shape)

    logging.info("Extraction finished")
    return json.dumps(datasets_dict, indent=4)
    #df.to_csv('opt/airflow/outputs/data.csv')

def transform(json_data, columns, add_id=False):
    """ Transform the data extracted from the datasets. """
        
    json_data = json.loads(json_data)
    dataframes_dict = dict()
    
    for key in json_data.keys():
        year = str(key)
        dataset = pd.json_normalize(json_data[year])
        dataset[f'year'] = year
        dataset.columns = get_columns(year)
        dataframes_dict[year] = dataset.to_dict(orient='records')
        
    return json.dumps(dataframes_dict, indent=4)

def concatenate(json_data):
    """ Concatenate the datasets. """
    
    json_data = json.loads(json_data)

    concatenated_dataframe = pd.concat([pd.json_normalize(json_data[year]) for year in json_data.keys()], ignore_index=True)

    logging.info('Data concatenated has ', concatenated_dataframe.shape)
    return concatenated_dataframe.to_json(orient='records')

def transform_concatenated(json_data):
    """ Transform the concatenated data. """
    
    json_data = json.loads(json_data)
    concatenated_dataframe = pd.json_normalize(json_data)
    
    concatenated_dataframe['region'] = concatenated_dataframe['country'].map(get_region_by_country())
    concatenated_dataframe['country_region'] = concatenated_dataframe['country'].fillna('') + ' - ' + concatenated_dataframe['region'].fillna('')
    concatenated_dataframe['country_region'] = concatenated_dataframe['country_region'].str.strip(' -')

    concatenated_dataframe.index += 1
    concatenated_dataframe.reset_index(inplace=True)
    concatenated_dataframe.rename(columns={'index': 'id'}, inplace=True)
    
    logging.info('Data concatenated transformed.')
    return concatenated_dataframe.to_json(orient='records')

def data_streaming(json_data):
    """ Stream the data via Kafka. """
    
    json_data = json.loads(json_data)
    topic = 'viewer_kafka'
    dataframe_to_stream = pd.json_normalize(json_data)
    
    producer = kafka_producer()
    logging.info('Data in streaming.')
    producer.send(topic, value='-/Start/-')
    for index in range(len(dataframe_to_stream)):
        producer.send(topic, value=dataframe_to_stream.iloc[index].to_dict())
    producer.send(topic, value='-/End/-')
    producer.flush()
    producer.close()
    logging.info('End streaming.')
    

    
    