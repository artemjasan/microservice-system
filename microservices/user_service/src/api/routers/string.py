import typing as t
from uuid import UUID

import fastapi

from src.api.dependencies import (
    unit_of_work as unit_of_work_dependency,
    string_service as string_service_dependency,
)
from src.database.unit_of_work import UnitOfWork
from src.services.string_services import StringService

string_router = fastapi.APIRouter(
    prefix="/string",
    tags=[
        "string",
    ],
)


@string_router.get("/register")
async def register_string(
    string_service: StringService = fastapi.Depends(string_service_dependency),
):
    pass


@string_router.get("/status")
async def get_event_status(
    uuid: UUID,
    string_service: StringService = fastapi.Depends(string_service_dependency),
):
    pass
