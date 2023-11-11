import asyncio

from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage, AbstractChannel

from reverse_src.schemas import ServiceMessage


async def message_consuming(message: AbstractIncomingMessage, queue: asyncio.Queue) -> None:
    reverted_message = await _message_reverting(_message_validation(message))
    await queue.put(reverted_message)


async def message_publishing(channel: AbstractChannel, message: ServiceMessage, routing_key: str) -> None:
    await channel.default_exchange.publish(
        Message(**message.serialize()),
        routing_key=routing_key,
    )


def _message_validation(message: AbstractIncomingMessage) -> ServiceMessage:
    return ServiceMessage(uuid=message.message_id, body=message.body.decode("utf-8"))


async def _message_reverting(message: ServiceMessage, sleep_time: int = 5) -> ServiceMessage:
    await asyncio.sleep(sleep_time)
    message.revert_body()
    return message
