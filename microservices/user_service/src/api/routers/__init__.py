"""Routers for FastAPI server."""
from src.api.routers.health import healthcheck_router
from src.api.routers.string import string_router

ALL_ROUTERS = [
    healthcheck_router,
    string_router,
]


__all__ = [
    "ALL_ROUTERS",
]
