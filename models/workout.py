from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.set import ExerciseSet


class WorkoutStatus(enum.StrEnum):
    active = "active"
    finished = "finished"


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    status: Mapped[WorkoutStatus] = mapped_column(Enum(WorkoutStatus), nullable=False, default=WorkoutStatus.active)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    sets: Mapped[list[ExerciseSet]] = relationship(back_populates="session")
