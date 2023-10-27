from settings import RabbitMQSettings


def dsn_from_settings(settings: RabbitMQSettings) -> str:
    """Prepare connections string for RabbitMQ."""
    protocol = "amqp"
    return f"{protocol}://{settings.DEFAULT_USER}:{settings.DEFAULT_PASS}@{settings.HOST}"
