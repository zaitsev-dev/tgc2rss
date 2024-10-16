from datetime import datetime
from xml.etree.ElementTree import ParseError, fromstring

from pydantic import BaseModel, HttpUrl, constr, field_validator
from pydantic_core.core_schema import ValidationInfo


class RSSFeed(BaseModel):
    """RSS feed"""

    title: constr(min_length=1)
    link: HttpUrl
    description: constr(min_length=1)
    items: list['RSSItem']
    language: constr(min_length=2, max_length=2) | None = None
    last_build_date: datetime | None = None


class RSSItem(BaseModel):
    """Item of RSS feed"""

    title: constr(min_length=1)
    link: HttpUrl
    description: constr(min_length=1)
    author: constr(min_length=1) | None = None
    category: constr(min_length=1) | None = None
    guid: constr(min_length=1) | None = None
    pub_date: datetime | None = None


class XMLFeed(BaseModel):
    """RSS feed presented as XML code"""

    rss_model: RSSFeed
    xml: constr(min_length=1)

    @field_validator('xml')
    @classmethod
    def validate_xml(cls, value: str, _: ValidationInfo):
        """Validate xml field is valid XML code"""
        try:
            fromstring(value)
        except ParseError as e:
            raise ValueError('Invalid XML format') from e
        return value
