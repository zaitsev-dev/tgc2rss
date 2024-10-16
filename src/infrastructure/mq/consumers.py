from collections.abc import Callable
from typing import Any

from confluent_kafka import Consumer, KafkaException, Message
from loguru import logger

from config import config

conf = {
    'bootstrap.servers': f'{config.kafka_address}:{config.kafka_port}',
    'group.id': 'my_group',
}
consumer = Consumer(conf)


def poll_messages(topics: list[str], callback: Callable[[Message], Any]):
    """Poll Kafka for specified topics

    Parameters
    ----------
        topics: list of topics to consume
        callback: handling callback for a message

    """
    consumer.subscribe(topics)

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            msg_error = msg.error()
            if msg_error:
                raise KafkaException(msg_error)

            logger.debug(f'Received message from topic {msg.topic()}: {msg.value()}')

            try:
                callback(msg)
            except Exception as e:
                logger.error(f'Exception occurred: {e}')
    finally:
        consumer.close()
