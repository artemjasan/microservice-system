import asyncio
import contextlib
import logging
import signal
import typing

from aio_pika import Message, connect
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from reverse_src.message_schemas import ServiceMessage
from reverse_settings import ReverseSettings, dsn_from_settings

LOGGER = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def init_rmq_connection(settings: ReverseSettings) -> typing.AsyncContextManager[AbstractConnection]:
    async with contextlib.AsyncExitStack() as stack:
        connection = await stack.enter_async_context(await connect(dsn_from_settings(settings.rabbitmq)))
        yield connection


async def consumer(queue: asyncio.Queue, connection: AbstractConnection, queue_name: str) -> None:
    channel = await connection.channel()
    origin_queue = await channel.declare_queue(queue_name)

    async with origin_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process() as processed_message:
                await _on_message(processed_message, queue)

    LOGGER.info("Consumer task stopped or interrupted")


async def producer(queue: asyncio.Queue, connection: AbstractConnection, queue_name: str) -> None:
    channel = await connection.channel()
    processed_queue = await channel.declare_queue(queue_name)

    loop = asyncio.get_event_loop()
    stop_signal = loop.create_future()

    loop.add_signal_handler(signal.SIGINT, _signal_handler(stop_signal))
    loop.add_signal_handler(signal.SIGTERM, _signal_handler(stop_signal))

    while not stop_signal.done():
        data: ServiceMessage = await queue.get()
        await channel.default_exchange.publish(
            Message(**data.serialize()),
            routing_key=processed_queue.name,
        )
    LOGGER.info("Producer task stopped or interrupted")


async def _on_message(message: AbstractIncomingMessage, queue: asyncio.Queue) -> None:
    service_message = ServiceMessage(uuid=message.message_id, body=message.body.decode("utf-8"))
    service_message.revert_body()
    await asyncio.sleep(5)
    await queue.put(service_message)


def _signal_handler(stop_signal_: asyncio.Future) -> typing.Callable[[], None]:
    def handler():
        stop_signal_.set_result(None)

    return handler
