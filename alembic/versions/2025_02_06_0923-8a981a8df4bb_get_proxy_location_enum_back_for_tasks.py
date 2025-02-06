"""get proxy_location enum back for tasks

Revision ID: 8a981a8df4bb
Revises: ebf093461132
Create Date: 2025-02-06 09:23:24.003503+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8a981a8df4bb"
down_revision: Union[str, None] = "ebf093461132"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tasks",
        "proxy_location",
        existing_type=sa.VARCHAR(),
        type_=sa.Enum(
            "US_CA",
            "US_NY",
            "US_TX",
            "US_FL",
            "US_WA",
            "RESIDENTIAL",
            "RESIDENTIAL_ES",
            "RESIDENTIAL_IE",
            "RESIDENTIAL_GB",
            "RESIDENTIAL_IN",
            "RESIDENTIAL_JP",
            "RESIDENTIAL_FR",
            "RESIDENTIAL_DE",
            "NONE",
            name="proxylocation",
        ),
        postgresql_using="proxy_location::proxylocation",
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tasks",
        "proxy_location",
        existing_type=sa.Enum(
            "US_CA",
            "US_NY",
            "US_TX",
            "US_FL",
            "US_WA",
            "RESIDENTIAL",
            "RESIDENTIAL_ES",
            "RESIDENTIAL_IE",
            "RESIDENTIAL_GB",
            "RESIDENTIAL_IN",
            "RESIDENTIAL_JP",
            "RESIDENTIAL_FR",
            "RESIDENTIAL_DE",
            "NONE",
            name="proxylocation",
        ),
        type_=sa.VARCHAR(),
        postgresql_using="proxy_location::text",
        existing_nullable=True,
    )
    # ### end Alembic commands ###
