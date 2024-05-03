from contextlib import asynccontextmanager

from fastapi import FastAPI

# from app.api.routes.router import router as api_router
from app.core.config import get_app_settings
from app.api_v1 import router as router_v1

# from app.db.db_session import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    """Instanciating and setting up FastAPI application."""
    settings = get_app_settings()

    app = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)
    app.include_router(router=router_v1, prefix=settings.api_prefix)
    return app


"""def create_app():
    app = FastAPI(
        debug=True,
        docs_url='/api/docs',
        title='FastApi Example'
    )
    return app"""
