from uuid import UUID

import fastapi

from src.api.dependencies import string_service as string_service_dependency
from src.schemas.string_schemas import StringIDSchema, StringItemSchema
from src.services.string_services import StringService

string_router = fastapi.APIRouter(
    prefix="/string",
    tags=[
        "strings",
    ],
)


@string_router.get("/register")
async def register_string(
    string: str,
    string_service: StringService = fastapi.Depends(string_service_dependency),
) -> StringIDSchema:
    response = await string_service.register_string(string)
    return StringIDSchema.get_from_domain(response)


@string_router.get("/status")
async def get_event_status(
    uuid: UUID,
    string_service: StringService = fastapi.Depends(string_service_dependency),
) -> StringItemSchema:
    response = await string_service.get_string(uuid)
    return StringItemSchema.get_from_domain(response)
