import asyncio

from aio_pika import Message
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage

from src.message_schemas import ServiceMessage


async def consumer(queue: asyncio.Queue, connection: AbstractConnection, queue_name: str) -> None:
    async with connection:
        channel = await connection.channel()
        origin_queue = await channel.declare_queue(queue_name)

        async with origin_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process() as processed_message:
                    await _on_message(processed_message, queue)


async def producer(queue: asyncio.Queue, connection: AbstractConnection, queue_name: str) -> None:
    async with connection:
        channel = await connection.channel()
        processed_queue = await channel.declare_queue(queue_name)

        while True:
            data: ServiceMessage = await queue.get()
            await channel.default_exchange.publish(
                Message(**data.convert_to_rabbitmq_message_dict()),
                routing_key=processed_queue.name,
            )


async def _on_message(message: AbstractIncomingMessage, queue: asyncio.Queue) -> None:
    service_message = ServiceMessage(uuid=message.message_id, body=message.body.decode("utf-8"))
    service_message.revert_body()
    await asyncio.sleep(5)
    await queue.put(service_message)
