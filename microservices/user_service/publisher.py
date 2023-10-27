import asyncio
import uuid

from aio_pika import Message, connect
from settings import ApiSettings
from src.eventbus.connection import dsn_from_settings


async def main() -> None:
    # Perform connection
    settings = ApiSettings()

    connection = await connect(dsn_from_settings(settings.rabbitmq))

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("hello")
        counter = 0
        while True:
            counter += 1
            message = f"Hello World! {counter}"
            # Sending the message
            await channel.default_exchange.publish(
                Message(
                    message.encode(),
                    message_id=str(uuid.uuid4()),
                ),
                routing_key=queue.name,
            )
            print(f"[x] Sent {message}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
