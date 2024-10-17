from abc import ABC, abstractmethod

from domain.models import RSSFeed, XMLFeed


class IRssModelAdapter(ABC):
    """Interface of RSS model adapter"""

    @abstractmethod
    def convert(self, model: RSSFeed) -> XMLFeed:
        """Convert the model"""
