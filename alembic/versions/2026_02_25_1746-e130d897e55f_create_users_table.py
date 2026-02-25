"""create_users_table

Revision ID: e130d897e55f
Revises:
Create Date: 2026-02-25 17:46:08.772630

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e130d897e55f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True, autoincrement=True),
        sa.Column("firstname", sa.String(100), nullable=False),
        sa.Column("lastname", sa.String(100), nullable=False),
        sa.Column("date_of_birth", sa.DATE, nullable=False),
    )


def downgrade():
    op.drop_table("users")
