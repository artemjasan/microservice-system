import asyncio
import logging

import aio_pika
from reverse_settings import ReverseSettings, dsn_from_settings
from reverse_src.handlers import consumer, producer

LOGGER = logging.getLogger("ReverseService")


async def main(settings: ReverseSettings) -> None:
    connection = await aio_pika.connect(dsn_from_settings(settings.rabbitmq))
    queue = asyncio.Queue()

    tasks = [
        asyncio.create_task(consumer(queue, connection, settings.rabbitmq.ORIGIN_QUEUE)),
        asyncio.create_task(producer(queue, connection, settings.rabbitmq.PROCESSED_QUEUE)),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    LOGGER.info("Started reverse service")
    asyncio.run(main(ReverseSettings()))
