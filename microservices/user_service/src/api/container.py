"""Implement Dependency Injection container for API."""
import contextlib
import typing as t

from microservices.user_service.src.database.unit_of_work import UnitOfWork, UowFactory


class ApiContainer:
    """DI container for backend API."""

    def __init__(self, uow_factory: UowFactory) -> None:
        self._uow_factory = uow_factory

    @property
    @contextlib.asynccontextmanager
    async def uow(self) -> t.AsyncIterator[UnitOfWork]:
        """Provide UnitOfWork."""
        async with self._uow_factory() as uow:
            yield uow
