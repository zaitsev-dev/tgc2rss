from collections.abc import Callable

from confluent_kafka import Producer
from loguru import logger

from config import config

conf = {
    'bootstrap.servers': f'{config.kafka_address}:{config.kafka_port}',
}
producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        logger.warning(f'Message delivery failed: {err}')
    else:
        logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def send_message(topic: str, message: str, callback: Callable = delivery_report):
    producer.produce(topic, value=message, callback=callback)
    producer.flush()
