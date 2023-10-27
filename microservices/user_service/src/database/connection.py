import asyncio
import contextlib
import typing as t

import sqlalchemy as sa
from settings import PostgresSettings
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def dsn_from_settings(settings: PostgresSettings) -> str:
    """Prepare connections string for PostgreSQL."""
    protocol = "postgresql+asyncpg"
    return f"{protocol}://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT!s}/{settings.DB}"


def _make_engine(settings: PostgresSettings) -> AsyncEngine:
    """Make SQLAlchemy async engine."""

    return create_async_engine(
        url=dsn_from_settings(settings),
        pool_size=settings.POOL_SIZE,
    )


async def _ping_server(engine: AsyncEngine, n_attempts: int = 10) -> None:
    """Ping DB server to check connection liveness."""
    for attempt in range(1, n_attempts + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(sa.text("SELECT 1;"))
        except OSError:
            if attempt >= n_attempts:
                raise
            await asyncio.sleep(5)
        else:
            break


@contextlib.asynccontextmanager
async def psql_engine_ctx(settings: PostgresSettings, n_attempts: int = 10) -> t.AsyncIterator[AsyncEngine]:
    """Get context-managed connection to PostgreSQL server.

    Use it in async context manager to ensure the connection is
    correctly closed when it goes out of scope.
    """
    engine = _make_engine(settings)

    # Establish the first connection. This is not needed, but it ensures that the engine
    # is configured correctly and able to connect to the PG server.
    await _ping_server(engine, n_attempts)

    try:
        yield engine
    finally:
        await engine.dispose()
