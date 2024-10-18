from aiokafka import ConsumerRecord
from loguru import logger

from config import config
from domain.services.rss_parser import ChannelToRssParser
from infrastructure.adapters import RssModelToXmlAdapter
from infrastructure.repositories.telegram import TelegramRepository

from .producers import send_message


async def handle_channel_message(msg: ConsumerRecord) -> None:
    """Handle messages from channels topic"""
    telegram = TelegramRepository(api_id=config.bot_api_id, api_hash=config.bot_api_hash)
    service = ChannelToRssParser(telegram, adapter_class=RssModelToXmlAdapter())

    channel_username = msg.value.decode()
    logger.info(f'Got a channel from queue: {channel_username}')

    feed = await service.feed_to_xml(await service.parse_channel(channel_username))
    json = feed.model_dump_json().encode()
    await send_message('feeds', message=json)
