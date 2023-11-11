import asyncio
import logging

from reverse_settings import ReverseSettings
from reverse_src import handlers
from reverse_src import dependencies

LOGGER = logging.getLogger("ReverseService")


async def main(settings: ReverseSettings) -> None:
    async with dependencies.init_di_container(settings) as di_container:
        tasks = [
            asyncio.create_task(handlers.consumer(di_container)),
            asyncio.create_task(handlers.producer(di_container)),
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    LOGGER.info("Starting reverse service...")
    asyncio.run(main(ReverseSettings()))
