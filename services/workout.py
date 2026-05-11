from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.workout import WorkoutSession, WorkoutStatus


async def get_active_session(db: AsyncSession, user_id: int) -> WorkoutSession | None:
    result = await db.execute(
        select(WorkoutSession).where(
            WorkoutSession.user_id == user_id,
            WorkoutSession.status == WorkoutStatus.active,
        )
    )
    return result.scalar_one_or_none()


async def start_session(db: AsyncSession, user_id: int) -> WorkoutSession:
    existing = await get_active_session(db, user_id)
    if existing:
        return existing

    session = WorkoutSession(user_id=user_id, status=WorkoutStatus.active)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def finish_session(db: AsyncSession, user_id: int) -> WorkoutSession | None:
    session = await get_active_session(db, user_id)
    if not session:
        return None

    session.status = WorkoutStatus.finished
    session.finished_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(session)
    return session
