import dataclasses
import uuid

from src.domain.application_enums import StringItemStatus


@dataclasses.dataclass
class StringItem:
    uuid: uuid.UUID
    body: str
    status: StringItemStatus
