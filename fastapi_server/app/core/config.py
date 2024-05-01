from os import getenv
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = 'postgresql+asyncpg://user:password@host:port/dbname[?key=value&key=value...]'

settings = Setting()
