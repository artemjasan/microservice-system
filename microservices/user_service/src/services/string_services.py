import uuid

from src.repository.string_repositories import StringRepository
from src.domain.models import StringItem


class StringService:
    def __init__(
        self,
        repository: StringRepository,
    ) -> None:
        self._repository = repository

    async def register_string(self, string: str) -> StringItem:
        response = await self._repository.register_string(string)
        return response

    async def get_string(self, id_: uuid.UUID) -> StringItem:
        return await self._repository.get_string(id_)
