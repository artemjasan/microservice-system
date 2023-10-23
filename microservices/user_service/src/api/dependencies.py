import typing as t

import fastapi

from microservices.user_service.src.api.container import ApiContainer
from microservices.user_service.src.database.unit_of_work import UnitOfWork
from microservices.user_service.src.services.string_services import StringService


async def unit_of_work(request: fastapi.Request) -> t.AsyncIterator[UnitOfWork]:
    """Dependency for Unit of Work."""
    container: ApiContainer = request.app.state.container
    async with container.uow as uow:
        yield uow


async def string_service(request: fastapi.Request) -> t.AsyncIterator[StringService]:
    """Dependency for StringService."""
    container: ApiContainer = request.app.state.container
    async with container.uow as uow:
        yield StringService(uow.string_repository, container.kafka_producer)
