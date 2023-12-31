import abc
import contextlib
import typing as t

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from src.repository.string_repositories import StringRepository, StringPostgresRepository


class UnitOfWork(abc.ABC):
    """Abstraction over DB connection."""

    @abc.abstractmethod
    async def is_ready(self) -> bool:
        """Check if DB connection is ready."""
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def string_repository(self) -> StringRepository:
        raise NotImplementedError()


class PsqlUnitOfWork(UnitOfWork):
    """PostgresSQL's implementation of Unit of Work."""

    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def is_ready(self) -> bool:
        """Check if DB connection is ready."""
        try:
            await self._connection.execute(sa.text("SELECT 1"))
        except sa.exc.SQLAlchemyError:
            return False

        return True

    @property
    def string_repository(self) -> StringPostgresRepository:
        return StringPostgresRepository(self._connection)


@contextlib.asynccontextmanager
async def psql_uow_factory(async_engine: AsyncEngine) -> t.AsyncIterator[PsqlUnitOfWork]:
    """Open new connection to PSQL server with active transaction."""
    async with async_engine.begin() as conn:
        yield PsqlUnitOfWork(conn)


UowFactory = t.Callable[[], t.AsyncContextManager[UnitOfWork]]
