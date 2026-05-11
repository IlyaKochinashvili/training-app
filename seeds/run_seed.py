import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import settings
from models.exercise import Exercise
from models.exercise_alias import ExerciseAlias
from seeds.exercises import EXERCISES


async def seed(session: AsyncSession) -> None:
    for name_uk, muscle_group, aliases in EXERCISES:
        exercise = Exercise(name_uk=name_uk, muscle_group=muscle_group)
        session.add(exercise)
        await session.flush()

        for alias_text, language in aliases:
            session.add(ExerciseAlias(exercise_id=exercise.id, alias=alias_text, language=language))

    await session.commit()
    print(f"Seeded {len(EXERCISES)} exercises")


async def main() -> None:
    engine = create_async_engine(settings.database_url)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        await seed(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
