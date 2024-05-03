"""Settings that will be used throughout the application."""
import logging
import os
import sys
from typing import Any, Dict, List, Tuple
from dotenv import load_dotenv
from pydantic import PostgresDsn
from sqlalchemy.engine.url import URL

from loguru import logger

from app.core.logging import format_record, InterceptHandler

load_dotenv()
class AppSettings():
    """Bundle all app settings."""
    # FastAPI App settings
    debug: bool = True
    docs_url: str = "/api/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    #openapi_tags: List[dict] = [tag.dict(by_alias=True) for tag in metadata_tags]
    #allowed_hosts: List[str] = ["*"]

    title: str = 'FastApi Example2'
    #version: str = os.getenv("APP_VERSION")
    #description: str = os.getenv("APP_DESCRIPTION")
    api_prefix: str = "/api/v1"

    # database settings
    postgres_driver: str = "asyncpg"
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: int = os.getenv("POSTGRES_PORT")
    postgres_db: str = os.getenv("POSTGRES_DB")
    # logging
    logging_level: int = logging.DEBUG
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "title": self.title,

        }

    @property
    def database_settings(self) -> Dict[str, Any]:
        return {
            "postgres_user": self.postgres_user,
            "postgres_password": self.postgres_password,
            "postgres_host": self.postgres_host,
            "postgres_port": self.postgres_port,
            "postgres_db": self.postgres_db,
        }

    @property
    def database_url(self) -> PostgresDsn:
        """Create a valid Postgres database url."""
        logger.success(f'pizda{self.postgres_user, self.postgres_password, self.postgres_host, self.postgres_port, self.postgres_db}')
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.postgres_host,
            database=self.postgres_db,
            username=self.postgres_user,
            password=self.postgres_password,
            port=self.postgres_port
        )

    def configure_logging(self) -> None:
        """Configure and format logging used in app."""
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        # intercept everything at the root logger
        logging.root.handlers = [InterceptHandler()]
        logging.root.setLevel("DEBUG")

        # remove every other logger's handlers
        # and propagate to root logger
        for name in logging.root.manager.loggerDict.keys():
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

        # configure loguru
        logger.configure(
            handlers=[{"sink": sys.stdout, "serialize": False, "format": format_record, "colorize": True, }])
