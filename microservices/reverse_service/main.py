import asyncio

from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage
from reverse_settings import ReverseSettings, dsn_from_settings
from services import get_required_queue, reverse


async def on_message(message: AbstractIncomingMessage, channel, target_queue) -> None:
    body = message.body.decode("utf-8")
    inverted_body = reverse(body)
    await channel.default_exchange.publish(
        Message(inverted_body.encode("utf-8")),
        routing_key=target_queue.name,
    )


async def main(settings: ReverseSettings) -> None:
    connection = await connect(dsn_from_settings(settings.rabbitmq))
    async with connection:
        channel = await connection.channel()

        origin_queue = await get_required_queue(channel, settings.rabbitmq.ORIGIN_QUEUE, auto_delete=True)
        processed_queue = await get_required_queue(channel, settings.rabbitmq.PROCESSED_QUEUE, auto_delete=True)

        # Start listening the source queue
        await origin_queue.consume(lambda message: on_message(message, channel, processed_queue))


if __name__ == "__main__":
    asyncio.run(main(ReverseSettings()))
