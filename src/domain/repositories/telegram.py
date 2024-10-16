from abc import ABC, abstractmethod

from domain.models import BlogPost, Channel


class ITelegramRepository(ABC):
    """Telegram repository interface"""

    @abstractmethod
    async def get_posts(self, channel: str, count: int) -> list[BlogPost]:
        """Get posts of channel"""

    @abstractmethod
    async def get_channel(self, channel: str) -> Channel:
        """Get channel"""
