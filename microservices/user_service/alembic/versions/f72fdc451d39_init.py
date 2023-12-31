"""init

Revision ID: f72fdc451d39
Revises: 774b416c247d
Create Date: 2023-10-25 21:01:20.370023

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f72fdc451d39"
down_revision: Union[str, None] = "774b416c247d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "strings",
        sa.Column(
            "uuid", sqlalchemy_utils.types.uuid.UUIDType(), server_default=sa.text("uuid_generate_v4()"), nullable=False
        ),
        sa.Column("body", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("strings")
    # ### end Alembic commands ###
