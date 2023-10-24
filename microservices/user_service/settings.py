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


class ApiSettings(BaseSettings):
    """Settings for API."""

    postgres: PostgresSettings = Field(
        default_factory=PostgresSettings,
    )
    sentry: SentrySettings = Field(
        default_factory=SentrySettings,
    )


class DbMigrationSettings(BaseSettings):
    """Settings for alembic, Db migration tool."""

    postgres: PostgresSettings = Field(
        default_factory=PostgresSettings,
    )
