import asyncio

from loguru import logger

from infrastructure.mq.consumers import poll_messages
from infrastructure.mq.handlers import handle_channel_message


async def main():
    """Entry point of application"""
    logger.info('Application has started')
    try:
        await poll_messages(topics=['channels'], callback=handle_channel_message)
    except KeyboardInterrupt:
        logger.info('Application has stopped')


if __name__ == '__main__':
    asyncio.run(main())
