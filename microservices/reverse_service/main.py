import asyncio
import logging

from reverse_settings import ReverseSettings
from reverse_src.handlers import consumer, producer, init_rmq_connection

LOGGER = logging.getLogger("ReverseService")


async def main(settings: ReverseSettings) -> None:
    queue = asyncio.Queue()
    async with init_rmq_connection(settings) as rmq_connection:
        tasks = [
            asyncio.create_task(consumer(queue, rmq_connection, settings.rabbitmq.ORIGIN_QUEUE)),
            asyncio.create_task(producer(queue, rmq_connection, settings.rabbitmq.PROCESSED_QUEUE)),
        ]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    LOGGER.info("Started reverse service")
    asyncio.run(main(ReverseSettings()))
