from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    """Settings for RabbitMQ"""

    model_config = SettingsConfigDict(
        env_prefix="RABBITMQ_",
    )

    HOST: str = "localhost"
    DEFAULT_USER: str = "guest"
    DEFAULT_PASS: str = "guest"
    ORIGIN_QUEUE: str = "origin"
    PROCESSED_QUEUE: str = "processed"


class ReverseSettings(BaseSettings):
    """Settings for API."""

    rabbitmq: RabbitMQSettings = Field(
        default_factory=RabbitMQSettings,
    )


def dsn_from_settings(settings: RabbitMQSettings) -> str:
    """Prepare connections string for RabbitMQ."""
    protocol = "amqp"
    return f"{protocol}://{settings.DEFAULT_USER}:{settings.DEFAULT_PASS}@{settings.HOST}"
