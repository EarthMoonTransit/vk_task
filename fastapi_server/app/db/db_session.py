"""Connection to the Postgres database."""

from asyncio import current_task
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError


from app.core.config import get_app_settings
from app.db.models.base import Base


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(
    url=get_app_settings().database_url,
    echo=True,
)


'''def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    async_engine = None
    try:
        logger.success(f"nY Davai{get_app_settings().database_url}")
        async_engine = create_async_engine(
            get_app_settings().database_url,
            future=True,
        )
    except SQLAlchemyError as e:
        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)

    return async_engine


# DB dependency
async def get_async_session():
    """Yield an async session.

    All conversations with the database are established via the session
    objects. Also. the sessions act as holding zone for ORM-mapped objects.
    """
    async_session = async_sessionmaker(
        bind=get_async_engine(),
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,  # document this
    )

    return async_session


async def get_scoped_session():
    session_fac = await get_async_session()
    session = async_scoped_session(session_factory=session_fac, scopefunc=current_task)
    return session


async def session_dependency() -> AsyncSession:
    session = await get_scoped_session()
    async with session as sess:
        yield sess
        await session.remove()


async def initialize_database() -> None:
    """Create table in metadata if they don't exist yet.

    This uses a sync connection because the 'create_all' doesn't
    feature async yet.
    """
    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(Base.metadata.create_all)

        logger.success("Initializing database was successfull.")'''
