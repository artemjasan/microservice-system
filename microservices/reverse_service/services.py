from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage, AbstractQueue


def reverse(body: str) -> str:
    """Reverse string."""
    return body[::-1]


async def get_required_queue(channel: AbstractChannel, queue_name: str, auto_delete: bool = False) -> AbstractQueue:
    """Get queue by name. If queue does not exist, create it."""
    return await channel.declare_queue(queue_name, auto_delete=auto_delete)


async def send_message(channel: AbstractChannel, queue: AbstractQueue, message: str) -> None:
    """Send message to queue."""
    await channel.default_exchange.publish(
        Message(message.encode("utf-8")),
        routing_key=queue.name,
    )


async def process_message(message: AbstractIncomingMessage) -> None:
    """High-level service for processing messages."""
    async with message.process():
        body = message.body.decode("utf-8")
        inverted_body = reverse(body)
        print(f" [x] Received {inverted_body}")
