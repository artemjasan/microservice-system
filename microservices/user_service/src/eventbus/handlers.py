from aio_pika.abc import AbstractIncomingMessage

from src.eventbus.dependencies import DIContainer
from src.domain.application_enums import StringItemStatus
from src.eventbus.schemas import ServiceMessage


async def consumer(di_container: DIContainer) -> None:
    channel = await di_container.rmq_connection.channel()  # noqa TODO: remove noqa
    processed_queue = await channel.declare_queue(di_container.processed_queue)

    async with processed_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process() as processed_message:
                await _on_message(processed_message, di_container)


async def _on_message(message: AbstractIncomingMessage, di_container: DIContainer) -> None:
    service_message = ServiceMessage(uuid=message.message_id, body=message.body.decode("utf-8"))
    async with di_container.uow as uow:
        await uow.string_repository.update_string(service_message.uuid, service_message.body, StringItemStatus.DONE)
