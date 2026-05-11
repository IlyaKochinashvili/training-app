"""add has_angle_variant to exercises

Revision ID: 003
Revises: 002
Create Date: 2026-05-11
"""

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: str | None = "002"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.add_column("exercises", sa.Column("has_angle_variant", sa.Boolean(), nullable=False, server_default="false"))


def downgrade() -> None:
    op.drop_column("exercises", "has_angle_variant")
