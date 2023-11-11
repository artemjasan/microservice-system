import asyncio
import contextlib
import dataclasses
import functools
import typing as t

from aio_pika import connect
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue

from reverse_settings import ReverseSettings, dsn_from_settings
from reverse_src.services import message_consuming, message_publishing


@dataclasses.dataclass
class DIContainer:
    rmq_connection: AbstractConnection
    queue: asyncio.Queue
    origin_queue: str
    processed_queue: str
    consume_message: functools.partial
    publish_message: functools.partial

    @property
    async def channel(self) -> AbstractChannel:
        return await self.rmq_connection.channel()

    async def get_origin_queue(self) -> AbstractQueue:
        channel = await self.channel
        return await channel.declare_queue(self.origin_queue)

    async def get_processed_queue(self) -> AbstractQueue:
        channel = await self.channel
        return await channel.declare_queue(self.processed_queue)


@contextlib.asynccontextmanager
async def init_di_container(settings: ReverseSettings) -> t.AsyncIterator[DIContainer]:
    async with contextlib.AsyncExitStack() as stack:
        connection = await stack.enter_async_context(await connect(dsn_from_settings(settings.rabbitmq)))
        queue = asyncio.Queue()
        yield DIContainer(
            rmq_connection=connection,
            queue=queue,
            origin_queue=settings.rabbitmq.ORIGIN_QUEUE,
            processed_queue=settings.rabbitmq.PROCESSED_QUEUE,
            consume_message=functools.partial(message_consuming, queue=queue),
            publish_message=functools.partial(message_publishing, routing_key=settings.rabbitmq.PROCESSED_QUEUE),
        )
