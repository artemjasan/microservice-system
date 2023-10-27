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


class ApiSettings(BaseSettings):
    """Settings for API."""

    postgres: PostgresSettings = Field(
        default_factory=PostgresSettings,
    )
    sentry: SentrySettings = Field(
        default_factory=SentrySettings,
    )

    rabbitmq: RabbitMQSettings = Field(
        default_factory=RabbitMQSettings,
    )


class DbMigrationSettings(BaseSettings):
    """Settings for alembic, Db migration tool."""

    postgres: PostgresSettings = Field(
        default_factory=PostgresSettings,
    )
