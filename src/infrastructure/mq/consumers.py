from collections.abc import Awaitable, Callable
from typing import Any

from confluent_kafka import Consumer, KafkaException, Message
from loguru import logger

from config import config

conf = {
    'bootstrap.servers': f'{config.kafka_address}:{config.kafka_port}',
    'group.id': 'my_group',
}
consumer = Consumer(conf)


async def poll_messages(topics: list[str], callback: Callable[[Message], Awaitable[Any]]):
    """Poll Kafka for specified topics

    Arguments:
        topics: list of topics to consume
        callback: handling callback for a message

    """
    consumer.subscribe(topics)
    logger.info('Start a message queue polling')

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
                await callback(msg)
            except Exception as e:
                logger.exception(e)
    finally:
        consumer.close()
