from abc import ABC, abstractmethod

from domain.models import RSSFeed


class IRssModelAdapter(ABC):
    """Interface of RSS model adapter"""

    @abstractmethod
    def convert(self, model: RSSFeed):
        """Convert the model"""
