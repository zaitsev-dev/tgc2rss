from domain.adapters import IRssModelAdapter
from domain.models import RSSFeed


class RssModelToXmlAdapter(IRssModelAdapter):
    """Convert RSSFeed model to XML code"""

    def convert(cls, model: RSSFeed): ...  # TODO: implement it
