import contextlib
import functools
import logging
import typing as t

import sentry_sdk
from fastapi import FastAPI
from settings import ApiSettings, SentrySettings
from src.api.container import ApiContainer
from src.api.routers import ALL_ROUTERS
from src.database.connection import psql_engine_ctx
from src.database.unit_of_work import psql_uow_factory

LOGGER = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def default_api_lifespan(app: FastAPI, settings: ApiSettings) -> t.AsyncIterator[None]:
    """Default lifespan function for API server.

    This function is responsible for initializing all services required
    by the API server and putting them to Dependency Injeciton
    container.

    The container should be put into ``app.state.container`` attribute.
    This is especially relevant to alternate implementations of
    lifespan function, e.g., for testing.
    """
    async with contextlib.AsyncExitStack() as stack:
        psql_engine = await stack.enter_async_context(psql_engine_ctx(settings.postgres))
        uow_factory = functools.partial(psql_uow_factory, psql_engine)
        app.state.container = ApiContainer(
            uow_factory=uow_factory,
        )
        yield


def init_sentry(sentry_settings: SentrySettings) -> None:
    """Initialize sentry if configured."""
    if sentry_settings.dsn is None:
        LOGGER.warning("Sentry is not configured")
    else:
        LOGGER.info("Setting up sentry with %r", sentry_settings)
        sentry_sdk.init(
            dsn=sentry_settings.dsn,
            environment=sentry_settings.environment,
        )


LifespanCallable = t.Callable[[FastAPI, ApiSettings], t.AsyncContextManager[None]]


def make_app(lifespan_callable: LifespanCallable | None = None) -> FastAPI:
    """API factory.

    Lifespan function can be passed so that we can alter what
    components are put into the API server.
    """
    settings = ApiSettings()
    # init_sentry(settings.sentry)
    app = FastAPI(
        lifespan=functools.partial(
            lifespan_callable or default_api_lifespan,
            settings=settings,
        ),
    )

    for router in ALL_ROUTERS:
        app.include_router(router)
    return app
