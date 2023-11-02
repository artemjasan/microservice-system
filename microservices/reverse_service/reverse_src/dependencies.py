import asyncio
import contextlib
import dataclasses
import typing as t

from aio_pika import connect
from aio_pika.abc import AbstractConnection

from reverse_settings import ReverseSettings, dsn_from_settings


@dataclasses.dataclass
class DIContainer:
    rmq_connection: AbstractConnection
    queue: asyncio.Queue
    origin_queue: str
    processed_queue: str


@contextlib.asynccontextmanager
async def init_di_container(settings: ReverseSettings) -> t.AsyncIterator[DIContainer]:
    async with contextlib.AsyncExitStack() as stack:
        connection = await stack.enter_async_context(await connect(dsn_from_settings(settings.rabbitmq)))
        yield DIContainer(
            rmq_connection=connection,
            queue=asyncio.Queue(),
            origin_queue=settings.rabbitmq.ORIGIN_QUEUE,
            processed_queue=settings.rabbitmq.PROCESSED_QUEUE,
        )
