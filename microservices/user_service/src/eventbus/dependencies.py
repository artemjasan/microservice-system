import typing as t
import contextlib
import functools

from aio_pika import connect
from aio_pika.abc import AbstractConnection

from settings import ApiSettings
from src.database.connection import psql_engine_ctx
from src.database.unit_of_work import psql_uow_factory, UowFactory, UnitOfWork
from src.eventbus.connection import dsn_from_settings


class DIContainer:
    def __init__(
            self,
            uow_factory: UowFactory,
            rmq_connection: AbstractConnection,
            origin_queue: str,
            processed_queue: str
    ) -> None:
        self._uow_factory = uow_factory
        self._rmq_connection = rmq_connection
        self.origin_queue = origin_queue
        self.processed_queue = processed_queue

    @property
    @contextlib.asynccontextmanager
    async def uow(self) -> t.AsyncIterator[UnitOfWork]:
        """Provide UnitOfWork."""
        async with self._uow_factory() as uow:
            yield uow


@contextlib.asynccontextmanager
async def init_di_container(settings: ApiSettings) -> t.AsyncIterator[DIContainer]:
    async with contextlib.AsyncExitStack() as stack:
        psql_engine = await stack.enter_async_context(psql_engine_ctx(settings.postgres))
        uow_factory = functools.partial(psql_uow_factory, psql_engine)
        rmq_connection = await stack.enter_async_context(await connect(dsn_from_settings(settings.rabbitmq)))

        yield DIContainer(
            uow_factory=uow_factory,
            origin_queue=settings.rabbitmq.ORIGIN_QUEUE,
            processed_queue=settings.rabbitmq.PROCESSED_QUEUE,
            rmq_connection=rmq_connection,
        )
