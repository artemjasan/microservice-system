"""Settings loader for application."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """PostgreSQL related settings."""

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
    )

    HOST: str = "localhost"
    PORT: int = 5432
    DB: str = "postgres"
    USER: str = "postgres"
    PASSWORD: str = "postgres"


class SentrySettings(BaseSettings):
    """Settings for observability, e.g., sentry."""

    model_config = SettingsConfigDict(
        env_prefix="SENTRY_",
    )

    dsn: str | None = None
    environment: str = "production"


# class KafkaSettings(BaseSettings):
#     """Settings for Kafka."""
#
#     model_config = SettingsConfigDict(
#         env_prefix="KAFKA_",
#     )
#
#     bootstrap_servers: str = "kafka:9092"
#     producer_topic: str = "test-topic-1"
#     consumer_topic: str = "test-topic-2"


class ApiSettings(BaseSettings):
    """Settings for API."""

    postgres: PostgresSettings = Field(
        default_factory=PostgresSettings,
    )
    sentry: SentrySettings = Field(
        default_factory=SentrySettings,
    )
    # kafka: KafkaSettings = Field(
    #     default_factory=KafkaSettings,
    # )
    #

class DbMigrationSettings(BaseSettings):
    """Settings for alembic, Db migration tool."""

    postgres: PostgresSettings = Field(
        default_factory=PostgresSettings,
    )
