from textwrap import shorten

import bs4
import mistletoe

from domain.adapters import IRssModelAdapter
from domain.models import RSSFeed, RSSItem
from domain.repositories import ITelegramRepository


class ChannelToRssParser:
    """Service to perform Telegram channel as RSS feed"""

    def __init__(self, telegram: ITelegramRepository, adapter_class: IRssModelAdapter, feed_size: int = 10):
        """Initialize an instance

        Parameters
        ----------
            telegram: Service for working with Telegram
            adapter_class: A class of adapter that converts RSSFeed to XML code

        """
        self.telegram = telegram
        self.adapter = adapter_class
        self.feed_size = feed_size

    async def parse_channel(self, channel: str) -> RSSFeed:
        """Get channel posts and return a feed from those posts

        Parameters
        ----------
            channel: link or channel username

        """
        posts = await self.telegram.get_posts(channel, count=self.feed_size)

        items = []
        for post in posts:
            content = self._markdown_to_html(post.content)
            title, description = self._extract_title(content)
            items.append(
                RSSItem(
                    title=title,
                    description=description,
                    link=post.link,
                )
            )

        channel = await self.telegram.get_channel(channel)
        return RSSFeed(
            title=channel.title,
            link=channel.url,
            description=channel.description,
            items=items,
        )

    def feed_to_xml(self, feed: RSSFeed) -> str:
        """Convert RSSFeed to XML code

        Parameters
        ----------
            feed: feed model

        """
        return self.adapter.convert(feed)

    @classmethod
    def _extract_title(cls, content: str) -> tuple[str, str]:
        lines = content.split('\n\n')
        if len(lines) > 1:
            title = cls._html_to_plain_text(lines[0])
            description = '\n\n'.join(lines[1:])
        else:
            title = cls._html_to_plain_text(content)
            description = content

        return shorten(title, width=160, placeholder='...'), description

    @classmethod
    def _markdown_to_html(cls, markup: str) -> str:
        return mistletoe.markdown(markup)

    @classmethod
    def _html_to_plain_text(cls, markup: str) -> str:
        return bs4.BeautifulSoup(markup, 'html.parser').text
