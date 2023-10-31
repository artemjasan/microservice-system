import asyncio
import logging
import signal
import typing

from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage

from reverse_src.dependencies import DIContainer
from reverse_src.message_schemas import ServiceMessage

LOGGER = logging.getLogger(__name__)


async def consumer(di_container: DIContainer) -> None:
    channel = await di_container.rmq_connection.channel()
    origin_queue = await channel.declare_queue(di_container.origin_queue)

    async with origin_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process() as processed_message:
                await _on_message(processed_message, di_container.queue)

    LOGGER.info("Consumer task stopped or interrupted")


async def producer(di_container: DIContainer) -> None:
    channel = await di_container.rmq_connection.channel()
    processed_queue = await channel.declare_queue(di_container.processed_queue)

    loop = asyncio.get_event_loop()
    stop_signal = loop.create_future()

    loop.add_signal_handler(signal.SIGINT, _signal_handler(stop_signal))
    loop.add_signal_handler(signal.SIGTERM, _signal_handler(stop_signal))

    while not stop_signal.done():
        data: ServiceMessage = await di_container.queue.get()
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
