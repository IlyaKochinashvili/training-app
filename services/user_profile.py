from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_profile import Sex, UserProfile


async def get_profile(db: AsyncSession, user_id: int) -> UserProfile | None:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    return result.scalar_one_or_none()


async def create_profile(
    db: AsyncSession,
    user_id: int,
    height_cm: int,
    weight_kg: float,
    age: int,
    sex: Sex,
) -> UserProfile:
    profile = UserProfile(user_id=user_id, height_cm=height_cm, weight_kg=weight_kg, age=age, sex=sex)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile
