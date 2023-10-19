"""Connection utilities for DB engine."""
import contextlib
import typing as t

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from microservices.user_service.settings import PostgresSettings


def dsn_from_settings(settings: PostgresSettings) -> str:
    """Prepare connections string for PostgreSQL."""
    protocol = "postgresql+asyncpg"
    return f"{protocol}://{settings.user}:{settings.password}@{settings.host}:{settings.port!s}/{settings.db}"


@contextlib.asynccontextmanager
async def psql_engine_ctx(settings: PostgresSettings) -> t.AsyncIterator[AsyncEngine]:
    """Get context-managed connection to PostgreSQL server.

    Use it in async context manager to ensure the connection is
    correctly closed when it goes out of scope.
    """
    engine = create_async_engine(
        url=dsn_from_settings(settings),
        pool_size=10,
    )
    async with engine.begin() as connection:
        await connection.execute(sa.text("SELECT 1"))

    try:
        yield engine
    finally:
        await engine.dispose()
