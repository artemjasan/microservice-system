"""Health-check endpoints."""
import typing as t

import fastapi

from src.api.dependencies import unit_of_work as unit_of_work_dependency
from src.database.unit_of_work import UnitOfWork

healthcheck_router = fastapi.APIRouter(
    prefix="/-",
    tags=[
        "health",
    ],
)


@healthcheck_router.get("/liveness")
async def liveness() -> dict[str, str]:
    """Tell the liveness probe that service is alive."""
    return {"status": "ok"}


@healthcheck_router.get("/readiness")
async def readiness(
    unit_of_work: t.Annotated[UnitOfWork, fastapi.Depends(unit_of_work_dependency)],
) -> dict[str, str]:
    """Tell the readiness probe that service is ready."""
    status = "success" if await unit_of_work.is_ready() else "failed"
    return {"status": status}
