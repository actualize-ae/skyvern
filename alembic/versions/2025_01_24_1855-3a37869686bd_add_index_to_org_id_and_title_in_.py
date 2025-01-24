"""Add index to org_id and title in workflows table

Revision ID: 3a37869686bd
Revises: 13e4af5c975c
Create Date: 2025-01-24 18:55:13.047159+00:00

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3a37869686bd"
down_revision: Union[str, None] = "13e4af5c975c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("organization_id_title_idx", "workflows", ["organization_id", "title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("organization_id_title_idx", table_name="workflows")
    # ### end Alembic commands ###
