from telethon import TelegramClient
from telethon import functions as tl_functions
from telethon.tl.types import ChatFull

from domain.models import BlogPost, Channel
from domain.repositories.telegram import ITelegramRepository


class TelegramRepository(ITelegramRepository):
    """Telegram entities repository"""

    def __init__(self, api_id: int, api_hash: str):
        self._client = TelegramClient('bot', api_id=api_id, api_hash=api_hash)

    def __del__(self):
        self._disconnect()

    async def get_posts(self, channel: str, count: int = 10) -> list[BlogPost]:
        """Get list of latest posts of channel

        Arguments:
            channel: link or username of channel
            count: count of posts to fetch

        """
        async with self._client as client:
            channel_obj = await client.get_entity(channel)
            messages = await client.get_messages(channel_obj, limit=count)

        posts: list[BlogPost] = []
        for message in messages:
            if message.text:  # TODO: add support for blank messages with media
                content = message.text
                url = f'https://t.me/c/{channel_obj.id}/{message.id}'
                posts.append(BlogPost(content=content, link=url))

        return posts

    async def get_channel(self, channel: str) -> Channel:
        """Get channel

        Arguments:
            channel: link or username of channel

        """
        async with self._client as client:
            obj = await client(tl_functions.channels.GetFullChannelRequest(channel=channel))
        title = obj.chats[0].title
        username = obj.chats[0].username
        desc = obj.full_chat.about
        link = self._generate_channel_link(obj)
        return Channel(title=title, username=username, description=desc, url=link)

    def _disconnect(self):
        if self._client.is_connected():
            self._client.disconnect()

    @classmethod
    def _generate_post_link(cls, channel, msg):
        return f'https://t.me/c/{channel.id}/{msg.id}'

    @classmethod
    def _generate_channel_link(cls, entity: ChatFull):
        info = entity.chats[0]
        base = 'https://t.me'
        if info.username:
            return f'{base}/{info.username}'
        return f'{base}/c/{info.id}/{info.access_hash}'
