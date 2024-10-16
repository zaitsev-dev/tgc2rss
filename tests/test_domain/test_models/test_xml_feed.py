from unittest.mock import MagicMock

from pytest import fixture, raises

from src.domain.models import RSSFeed, XMLFeed

VALID_XML_EXAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Example RSS Feed</title>
        <link>https://example.com</link>
        <description>This is an example description of an RSS feed.</description>
        <item>
            <title>First News</title>
            <link>https://example.com/news1</link>
            <description>Description of the first news.</description>
            <pubDate>Fri, 22 Sep 2023 10:00:00 +0000</pubDate>
        </item>
    </channel>
</rss>"""


@fixture(name='rss_feed')
def mocked_rss_feed():
    return MagicMock(spec=RSSFeed)


def test_invalid_xml(rss_feed):
    """Test model validation raise ValueError when XML code is invalid"""
    with raises(ValueError, match='Invalid XML format'):
        XMLFeed(rss_model=rss_feed, xml='<some invalid<< xml :))))>')


def test_valid_xml(rss_feed):
    """Test model validation is success with valid XML code"""
    XMLFeed(
        rss_model=rss_feed,
        xml=VALID_XML_EXAMPLE,
    )
