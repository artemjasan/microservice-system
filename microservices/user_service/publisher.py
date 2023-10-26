import asyncio

from aio_pika import Message, connect


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@rabbitmq/")

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
                Message(message.encode()),
                routing_key=queue.name,
            )
            print(f"[x] Sent {message}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
