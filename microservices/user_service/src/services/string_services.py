import typing
import uuid

from microservices.user_service.src.repository.string_repositories import StringRepository


class StringService:
    # TODO: Implement class attributes
    def __init__(
        self,
        repository: StringRepository,
        kafka_producer: typing.Any,  # TODO: Add correct type
    ) -> None:
        self._repository = repository
        self._kafka_producer = kafka_producer

    # TODO: Add correct return type
    def register_string(self, string: str) -> typing.Any:
        self._repository.register_string(string)
        self._kafka_producer.send_to_event_bus(string)

    # TODO: Add correct return type
    def get_event_status(self, id_: uuid.UUID) -> typing.Any:
        return self._repository.get_event_status(id_)
