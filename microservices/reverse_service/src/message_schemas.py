import uuid
from pydantic import BaseModel


class ServiceMessage(BaseModel):
    """Message for inter-service communication."""
    uuid: uuid.UUID
    body: str

    def revert_body(self) -> None:
        """Revert body."""
        self.body = self.body[::-1]

    def convert_to_rabbitmq_message_dict(self) -> dict[str, bytes | str]:
        """Convert to rabbitmq message dict format."""
        return {
            "body": self.body.encode(),
            "message_id": str(self.uuid),
        }
