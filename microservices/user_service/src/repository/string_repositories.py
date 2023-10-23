import abc
import typing
import uuid

from sqlalchemy.ext.asyncio import AsyncConnection


class StringRepository(abc.ABC):
    @abc.abstractmethod
    def register_string(self, string: str) -> None:  # TODO: Add correct return type
        pass

    @abc.abstractmethod
    def get_event_status(self, id_: uuid.UUID) -> typing.Any:  # TODO: Add correct return type
        pass


class StringPostgresRepository(StringRepository):
    def __init__(self, session: AsyncConnection) -> None:
        self._session = session

    def register_string(self, string: str) -> None:
        pass

    def get_event_status(self, id_: uuid.UUID) -> typing.Any:
        pass
