"""Settings loader for application."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """PostgreSQL related settings."""

    model_config = SettingsConfigDict(
        env_prefix="PSQL_",
    )

    host: str = "localhost"
    port: int = 5432
    db: str = "microservice_system_dev"
    user: str = "microservice_system_user"
    password: str = "microservice_system_pwd"


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
