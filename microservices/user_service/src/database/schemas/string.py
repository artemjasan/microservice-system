from sqlalchemy import Table, Column, String, text
from sqlalchemy_utils import UUIDType

from .base import metadata

string_table = Table(
    "strings",
    metadata,
    Column("uuid", UUIDType, primary_key=True, server_default=text("uuid_generate_v4()")),
    Column("body", String(128), nullable=False),
    Column("status", String, nullable=False, default="PENDING"),
)
