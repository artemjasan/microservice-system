import typing
import uuid

from pydantic import BaseModel

from src.domain.application_enums import StringItemStatus
from src.domain.models import StringItem


class StringIDSchema(BaseModel):
    uuid: uuid.UUID

    @classmethod
    def get_from_domain(cls, domain: StringItem) -> typing.Self:
        return cls(uuid=domain.uuid)


class StringItemSchema(StringIDSchema):
    body: str
    status: StringItemStatus

    @classmethod
    def get_from_domain(cls, domain: StringItem) -> typing.Self:
        return cls(uuid=domain.uuid, body=domain.body, status=domain.status)
