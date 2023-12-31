import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from settings import ApiSettings
from src.eventbus.connection import dsn_from_settings


async def on_message(message: AbstractIncomingMessage) -> None:
    """on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)

    print("Before sleep!")
    await asyncio.sleep(5)  # Represents async I/O operations
    print("After sleep!")


async def main() -> None:
    settings = ApiSettings()

    # Perform connection
    connection = await connect(dsn_from_settings(settings.rabbitmq))
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(settings.rabbitmq.PROCESSED_QUEUE)

        # Start listening the queue with name 'hello'
        await queue.consume(on_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
