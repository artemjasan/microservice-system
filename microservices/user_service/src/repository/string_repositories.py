import abc
import uuid

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import insert, select

from src.database.schemas.string import string_table
from src.domain.models import StringItem
from src.domain.exceptions import StringItemNotFoundError


class StringRepository(abc.ABC):
    @abc.abstractmethod
    async def register_string(self, string: str) -> StringItem:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_string(self, id_: uuid.UUID) -> StringItem:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_strings_by_status(self, status: str) -> list[StringItem]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update_string(self, id_: uuid.UUID, body: str, status: str) -> StringItem:
        raise NotImplementedError()


class StringPostgresRepository(StringRepository):
    def __init__(self, session: AsyncConnection) -> None:
        self._session = session

    async def register_string(self, string: str) -> StringItem:
        query = insert(string_table).values(body=string).returning(string_table)
        result = await self._session.execute(query)
        if row := result.fetchone():
            return StringItem(uuid=row.uuid, body=row.body, status=row.status)

        # TODO: think about better exception or if it is correct
        raise Exception("Something went wrong")

    async def get_string(self, id_: uuid.UUID) -> StringItem:
        query = select(string_table).where(string_table.c.uuid == id_)
        result = await self._session.execute(query)
        if row := result.fetchone():
            return StringItem(uuid=row.uuid, body=row.body, status=row.status)

        raise StringItemNotFoundError(f"String item with id: {id_} not found")

    async def get_strings_by_status(self, status: str) -> list[StringItem]:
        query = select(string_table).where(string_table.c.status == status)
        result = await self._session.execute(query)
        return [StringItem(uuid=row.uuid, body=row.body, status=row.status) for row in result.fetchall()]

    async def update_string(self, id_: uuid.UUID, body: str, status: str) -> StringItem:
        query = (
            string_table.update()
            .where(string_table.c.uuid == id_)
            .values(body=body, status=status)
            .returning(string_table)
        )
        result = await self._session.execute(query)
        if row := result.fetchone():
            return StringItem(uuid=row.uuid, body=row.body, status=row.status)

        raise StringItemNotFoundError(f"String item with id: {id_} not found")
