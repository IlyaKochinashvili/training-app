"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-11
"""

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name_uk", sa.String(200), nullable=False, unique=True),
        sa.Column(
            "muscle_group",
            sa.Enum("chest", "back", "legs", "shoulders", "arms", "core", name="musclegroup"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "exercise_aliases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False),
        sa.Column("alias", sa.String(200), nullable=False),
        sa.Column("language", sa.Enum("uk", "en", name="language"), nullable=False),
    )

    op.create_table(
        "workout_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), nullable=False, index=True),
        sa.Column(
            "status",
            sa.Enum("active", "finished", name="workoutstatus"),
            nullable=False,
            default="active",
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "exercise_sets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("workout_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("raw_input", sa.String(500), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("reps", sa.Integer(), nullable=False),
        sa.Column("rir", sa.Integer(), nullable=False, default=2),
        sa.Column("is_failure", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("exercise_sets")
    op.drop_table("workout_sessions")
    op.drop_table("exercise_aliases")
    op.drop_table("exercises")
    op.execute("DROP TYPE IF EXISTS musclegroup")
    op.execute("DROP TYPE IF EXISTS language")
    op.execute("DROP TYPE IF EXISTS workoutstatus")
