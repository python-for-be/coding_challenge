"""create_addresses_table

Revision ID: 2065c70a4d8d
Revises: e130d897e55f
Create Date: 2026-02-25 17:52:22.392530

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2065c70a4d8d"
down_revision: Union[str, Sequence[str], None] = "e130d897e55f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "addresses",
        sa.Column("user_id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("number", sa.String(10), nullable=False),
        sa.Column("street_name", sa.String(100), nullable=False),
        sa.Column("postcode", sa.String(20), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.ForeignKeyConstraint(
            columns=["user_id"], refcolumns=["users.id"], name="fk_addresses_user_id", ondelete="CASCADE"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("addresses")
