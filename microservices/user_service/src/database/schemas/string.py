from sqlalchemy import Table, Column, Integer, String

from .base import metadata

string_table = Table(
    "strings",
    metadata,
    Column("uuid", Integer, primary_key=True),
    Column("body", String(128), nullable=False),
    Column("status", String, nullable=False),
)
