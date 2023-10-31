import asyncio
import logging

from reverse_settings import ReverseSettings
from reverse_src.handlers import consumer, producer
from reverse_src.dependencies import init_di_container

LOGGER = logging.getLogger("ReverseService")


async def main(settings: ReverseSettings) -> None:
    async with asyncio.TaskGroup() as tg, init_di_container(settings) as di_container:
        tg.create_task(consumer(di_container))
        tg.create_task(producer(di_container))


if __name__ == "__main__":
    LOGGER.info("Starting reverse service...")
    asyncio.run(main(ReverseSettings()))
