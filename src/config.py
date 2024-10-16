from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ['config']


class Config(BaseSettings):
    """Model of application settings"""

    kafka_address: str
    kafka_port: str
    bot_api_id: int
    bot_api_hash: str

    model_config = SettingsConfigDict(env_file=('.env', '../.env'))


config = Config()
