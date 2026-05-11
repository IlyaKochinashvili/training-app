from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.exercise_alias import ExerciseAlias
    from models.set import ExerciseSet


class MuscleGroup(enum.StrEnum):
    chest = "chest"
    back = "back"
    legs = "legs"
    shoulders = "shoulders"
    arms = "arms"
    core = "core"


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_uk: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    muscle_group: Mapped[MuscleGroup] = mapped_column(Enum(MuscleGroup), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    aliases: Mapped[list[ExerciseAlias]] = relationship(back_populates="exercise", lazy="selectin")
    sets: Mapped[list[ExerciseSet]] = relationship(back_populates="exercise")
