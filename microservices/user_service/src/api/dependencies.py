"""Dependencies for API endpoint handers.

Examples of dependencies:
    * service providing business logic

        async def my_service(request: fastapi.Request) -> t.AsyncIterator[MyService]:
            \"""Dependency for AccountService.\"""
            container: ApiContainer = request.app.state.container
            async with container.uow as uow:
                yield MyService(uow.my_repository)
"""
import typing as t

import fastapi

from microservices.user_service.src.api.container import ApiContainer
from microservices.user_service.src.database.unit_of_work import UnitOfWork


async def unit_of_work(request: fastapi.Request) -> t.AsyncIterator[UnitOfWork]:
    """Dependency for Unit of Work."""
    container: ApiContainer = request.app.state.container
    async with container.uow as uow:
        yield uow
