"""Routers for FastAPI server."""
from src.api.routers.health import healthcheck_router

ALL_ROUTERS = [
    healthcheck_router,
]


__all__ = [
    "ALL_ROUTERS",
]
