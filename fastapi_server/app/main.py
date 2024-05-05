from fastapi import FastAPI

from app.core.app_settings import settings
from app.api_v1 import router as router_v1


def create_app() -> FastAPI:
    """Создание экземпляра и настройка приложения FastAPI."""

    app = FastAPI(**settings.fastapi_kwargs)
    app.include_router(router=router_v1, prefix=settings.api_prefix)
    return app


app = create_app()
