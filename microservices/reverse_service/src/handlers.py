import asyncio

from aio_pika.abc import AbstractConnection, AbstractIncomingMessage
from aio_pika import Message

from src.message_schemas import ServiceMessage


async def consumer(queue: asyncio.Queue, connection: AbstractConnection, queue_name: str) -> None:
    async with connection:
        channel = await connection.channel()
        origin_queue = await channel.declare_queue(queue_name)

        # Start listening the source queue
        await origin_queue.consume(lambda message: _on_message(message, queue))


async def producer(queue: asyncio.Queue, connection: AbstractConnection, queue_name: str) -> None:
    async with connection:
        channel = await connection.channel()
        reverse_queue = await channel.declare_queue(queue_name)

        while True:
            data: ServiceMessage = await queue.get()
            await channel.default_exchange.publish(
                Message(**data.convert_to_rabbitmq_message_dict()),
                routing_key=reverse_queue.name,
            )


async def _on_message(message: AbstractIncomingMessage, queue: asyncio.Queue) -> None:
    async with message.process():
        service_message_obj = ServiceMessage(uuid=message.message_id, body=message.body.decode("utf-8"))
        service_message_obj.revert_body()
        await asyncio.sleep(5)
        await queue.put(service_message_obj)
