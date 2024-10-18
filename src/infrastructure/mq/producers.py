from aiokafka import AIOKafkaProducer
from loguru import logger

from config import config


def delivery_report(err, msg):
    """Report a message delivery status"""
    if err is not None:
        logger.warning(f'Message delivery failed: {err}')
    else:
        logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')


async def send_message(topic: str, message: str | bytes):
    """Send a Kafka message to specified topic"""
    producer = AIOKafkaProducer(bootstrap_servers=f'{config.kafka_address}:{config.kafka_port}')
    await producer.start()
    try:
        await producer.send_and_wait(topic, message)
    finally:
        await producer.stop()
