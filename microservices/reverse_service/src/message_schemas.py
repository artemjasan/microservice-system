import uuid

from pydantic import BaseModel


class ServiceMessage(BaseModel):
    """Message for inner-service communication."""

    uuid: uuid.UUID
    body: str

    def revert_body(self) -> None:
        """Revert body."""
        self.body = self.body[::-1]

    def serialize(self) -> dict[str, bytes | str]:
        """Convert to dict format."""
        return {
            "body": self.body.encode(),
            "message_id": str(self.uuid),
        }
