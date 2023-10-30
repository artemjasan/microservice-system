import asyncio
import logging

import aio_pika

from settings import ApiSettings
from src.eventbus.connection import dsn_from_settings

LOGGER = logging.getLogger("UserService")


async def main(settings: ApiSettings) -> None:
    connection = await aio_pika.connect(dsn_from_settings(settings.rabbitmq))

    tasks = [
       # TODO: add tasks here (consumer, producer)
    ]

if __name__ == "__main__":
    LOGGER.info("Started user service")
    asyncio.run(main(ApiSettings()))
