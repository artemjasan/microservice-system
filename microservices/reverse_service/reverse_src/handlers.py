import logging
import typing as t

from reverse_src.dependencies import DIContainer
from reverse_src.schemas import ServiceMessage

LOGGER = logging.getLogger(__name__)


async def consumer(di_container: DIContainer) -> None:
    queue = await di_container.get_origin_queue()
    await queue.consume(di_container.consume_message)

    LOGGER.info("Consumer task stopped or interrupted")


async def producer(di_container: DIContainer) -> None:
    channel = await di_container.channel
    while True:
        message: ServiceMessage = await di_container.queue.get()
        await di_container.publish_message(channel=channel, message=message)
