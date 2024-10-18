from collections.abc import Awaitable, Callable
from typing import Any

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from loguru import logger

from config import config


async def poll_messages(topics: list[str], callback: Callable[[ConsumerRecord], Awaitable[Any]]):
    """Poll Kafka for specified topics

    Arguments:
        topics: list of topics to consume
        callback: handling callback for a message

    """
    consumer = AIOKafkaConsumer(
        *topics, bootstrap_servers=f'{config.kafka_address}:{config.kafka_port}', group_id='my_group'
    )

    await consumer.start()
    try:
        async for msg in consumer:
            logger.debug('Consumed: ', msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            try:
                await callback(msg)
            except Exception as e:
                logger.error(f'The error occurred while handling the message {msg}: {e}')
            else:
                await consumer.commit()
    finally:
        await consumer.stop()
