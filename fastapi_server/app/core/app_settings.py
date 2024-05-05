"""Settings that will be used throughout the application."""

import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv
from pydantic import PostgresDsn

BASE_DIR = Path(__file__).parent.parent


class AppSettings:
    """Все настройки приложения"""

    # FastAPI App settings
    debug: bool = True
    docs_url: str = "/api/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"

    title: str = "Vk Task"
    api_prefix: str = "/api/v1"
    load_dotenv(".env")

    # Database settings
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: int = os.getenv("POSTGRES_PORT")
    postgres_db: str = os.getenv("POSTGRES_DB")

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
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = AppSettings()
