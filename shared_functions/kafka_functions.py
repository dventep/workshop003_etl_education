""" This module contains functions for Kafka producer and consumer. """
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from json import dumps, loads
import logging

def create_topic(topic_name):
    """ Create a Kafka topic. """
    admin_client = KafkaAdminClient(
        bootstrap_servers = 'kafka_docker:9092'
        )
    # admin_client.create_topics(
    #     new_topics=[NewTopic(name = topic_name, num_partitions = 1, replication_factor = 1)],
    #     validate_only=False
    # )
    
    consumer = kafka_consumer()
    existing_topic_list = consumer.topics()
    topic_names = ['viewer_kafka']
    topic_list = []
    for topic in topic_names:
        if topic not in existing_topic_list:
            topic_list.append(NewTopic(name=topic, num_partitions=3, replication_factor=3))
    try:
        if topic_list:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except Exception as e:
        logging.error(f"Error creating topic: {e}")
    return True

def delete_topic(topic_name):
    """ Delete a Kafka topic. """
    admin_client = KafkaAdminClient(
        bootstrap_servers = 'kafka_docker:9092'
        )
    try:
        admin_client.delete_topics([topic_name])
    except Exception as e:
        pass
    return True

def kafka_producer():
    """ Create a Kafka producer. """
    producer = KafkaProducer(
        value_serializer = lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers = ['kafka_docker:9092'],
    )

    return producer

def kafka_consumer():
    """ Create a Kafka consumer. """
    
    consumer = KafkaConsumer(
        'viewer_kafka',
        enable_auto_commit=True,
        group_id='viewer_group',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['kafka_docker:9092']
    )
    
    return consumer

