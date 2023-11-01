import uuid

from pydantic import BaseModel


class ServiceMessage(BaseModel):
    uuid: uuid.UUID
    body: str

    def serialize(self) -> dict[str, bytes | str]:
        """Convert to dict format."""
        return {
            "body": self.body.encode(),
            "message_id": str(self.uuid),
        }
