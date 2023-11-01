import asyncio
import logging

from reverse_settings import ReverseSettings
from reverse_src import handlers
from reverse_src import dependencies

LOGGER = logging.getLogger("ReverseService")


async def main(settings: ReverseSettings) -> None:
    async with asyncio.TaskGroup() as tg, dependencies.init_di_container(settings) as di_container:
        tg.create_task(handlers.consumer(di_container))
        tg.create_task(handlers.producer(di_container))


if __name__ == "__main__":
    LOGGER.info("Starting reverse service...")
    asyncio.run(main(ReverseSettings()))
