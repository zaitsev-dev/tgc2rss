import asyncio

from confluent_kafka import Message
from loguru import logger

from infrastructure.mq.consumers import poll_messages
from infrastructure.mq.producers import send_message


def log_message(msg: Message):
    """Log message to loguru (or not?)"""
    logger.info(f'Got a message! See: {msg.value()}')
    send_message('test-out', message=f'I got your message! Msg: {msg.value()}')


async def main():
    """Entry point of application"""
    logger.info('Application has started')
    try:
        poll_messages(topics=['test-in'], callback=log_message)
    except KeyboardInterrupt:
        logger.info('Application has stopped')


if __name__ == '__main__':
    asyncio.run(main())
