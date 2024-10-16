from pydantic import BaseModel, HttpUrl, constr


class BlogPost(BaseModel):
    """Blog post of Telegram channel"""

    content: constr(min_length=1)
    link: HttpUrl


class Channel(BaseModel):
    """Telegram channel"""

    title: constr(min_length=1)
    username: constr(min_length=1)
    description: constr(min_length=1)
    url: HttpUrl | None = None
