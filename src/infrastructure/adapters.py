from xml.etree import ElementTree as ET

from domain.adapters import IRssModelAdapter
from domain.models import RSSFeed, RSSItem, XMLFeed


class RssModelToXmlAdapter(IRssModelAdapter):
    """Convert RSSFeed model to XML code"""

    RSS_VERSION = '2.0'

    def convert(self, model: RSSFeed) -> XMLFeed:
        """Convert RSSFeed to XMLFeed"""
        xml = self._build_xml(model)
        return XMLFeed(rss_model=model, xml=xml)

    @classmethod
    def _build_xml(cls, model: RSSFeed) -> str:
        root = ET.Element('rss', attrib={'version': cls.RSS_VERSION})
        channel = ET.SubElement(root, 'channel')
        ET.SubElement(channel, 'title', text=model.title)
        ET.SubElement(channel, 'link', text=str(model.link))
        ET.SubElement(channel, 'description', text=model.description)
        ET.SubElement(channel, 'lastBuildDate', text=model.last_build_date.strftime('%a, %d %b %y %H:%M:%S %z'))
        if (lang := model.language) is not None:
            ET.SubElement(channel, 'language', text=lang)

        for item in model.items:
            cls._append_item(parent=channel, model=item)

        return ET.tostring(root).decode()

    @classmethod
    def _append_item(cls, parent: ET.Element, model: RSSItem):
        item = ET.SubElement(parent, 'item')
        ET.SubElement(item, 'title', text=model.title)
        ET.SubElement(item, 'link', text=str(model.link))
        ET.SubElement(item, 'description', text=model.description)
