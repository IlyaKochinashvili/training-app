from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from services.exercise_parser import ParseError, parse_exercise_input
from services.exercise_resolver import is_trash, resolve_exercise
from services.workout import finish_session, get_active_session, start_session
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main import (
    BTN_FINISH_WORKOUT,
    BTN_START_WORKOUT,
    confirm_exercise_keyboard,
    confirm_finish_keyboard,
    main_menu,
    rir_keyboard,
    workout_menu,
)
from bot.states.workout import WorkoutFlow

router = Router()

# Loaded from DB during exercise resolution; keyed by user_id in FSM data
_CANDIDATES_KEY = "candidates"
_PARSED_KEY = "parsed_input"
_RESOLVED_KEY = "resolved_name"


async def _load_candidates(db: AsyncSession) -> list[tuple[str, list[str]]]:
    """Fetch all exercises with their aliases from DB."""
    from models.exercise import Exercise
    from sqlalchemy import select

    result = await db.execute(select(Exercise))
    exercises = result.scalars().all()
    return [(ex.name_uk, [a.alias for a in ex.aliases]) for ex in exercises]


@router.message(F.text == BTN_START_WORKOUT)
async def start_workout(message: Message, state: FSMContext, db: AsyncSession) -> None:
    session = await start_session(db, message.from_user.id)
    await state.set_state(WorkoutFlow.active)
    await message.answer(
        "💪 Тренування розпочато!\n\n"
        "Відправ вправу у форматі:\n"
        "<code>Назва вправи\nвага повтори\nвага повтори</code>\n\n"
        "Наприклад:\n"
        "<code>Жим лежачи\n100 8\n100 8\n95 6</code>",
        parse_mode="HTML",
        reply_markup=workout_menu(),
    )
    _ = session  # session is created, id available if needed


@router.message(WorkoutFlow.active, F.text == BTN_FINISH_WORKOUT)
async def ask_finish(message: Message, state: FSMContext) -> None:
    await state.set_state(WorkoutFlow.confirm_finish)
    await message.answer(
        "Завершити тренування?",
        reply_markup=confirm_finish_keyboard(),
    )


@router.callback_query(WorkoutFlow.confirm_finish, F.data == "finish:confirm")
async def finish_workout(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    session = await finish_session(db, callback.from_user.id)
    await state.clear()
    await callback.message.answer(
        "✅ Тренування завершено! Гарна робота 💪",
        reply_markup=main_menu(),
    )
    await callback.answer()
    _ = session


@router.callback_query(WorkoutFlow.confirm_finish, F.data == "finish:cancel")
async def cancel_finish(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(WorkoutFlow.active)
    await callback.message.answer("Продовжуємо 💪", reply_markup=workout_menu())
    await callback.answer()


@router.message(WorkoutFlow.active)
async def handle_exercise_input(message: Message, state: FSMContext, db: AsyncSession) -> None:
    try:
        parsed = parse_exercise_input(message.text or "")
    except ParseError as e:
        await message.answer(f"⚠️ {e}")
        return

    if is_trash(parsed.exercise_name):
        await message.answer("⚠️ Назва вправи виглядає некоректно. Спробуй ще раз.")
        return

    candidates = await _load_candidates(db)
    result = resolve_exercise(parsed.exercise_name, candidates)

    if result is None:
        await message.answer(f"❓ Не вдалось знайти вправу «{parsed.exercise_name}».\nПеревір назву або спробуй іншу.")
        return

    await state.update_data(**{_PARSED_KEY: _serialize_parsed(parsed), _RESOLVED_KEY: result.canonical_name})

    if result.is_exact:
        await state.set_state(WorkoutFlow.confirm_rir)
        await message.answer(
            f"✅ <b>{result.canonical_name}</b>\n{_format_sets_preview(parsed)}\n\nЯк відчувались підходи?",
            parse_mode="HTML",
            reply_markup=rir_keyboard(),
        )
    else:
        await state.set_state(WorkoutFlow.confirm_exercise)
        await message.answer(
            f"🤔 Можливо, ти маєш на увазі <b>{result.canonical_name}</b>?",
            parse_mode="HTML",
            reply_markup=confirm_exercise_keyboard(result.canonical_name),
        )


@router.callback_query(WorkoutFlow.confirm_exercise, F.data == "exercise:confirm")
async def confirmed_exercise(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(WorkoutFlow.confirm_rir)
    data = await state.get_data()
    parsed = _deserialize_parsed(data[_PARSED_KEY])
    canonical = data[_RESOLVED_KEY]
    await callback.message.answer(
        f"✅ <b>{canonical}</b>\n{_format_sets_preview(parsed)}\n\nЯк відчувались підходи?",
        parse_mode="HTML",
        reply_markup=rir_keyboard(),
    )
    await callback.answer()


@router.callback_query(WorkoutFlow.confirm_exercise, F.data == "exercise:reject")
async def rejected_exercise(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(WorkoutFlow.active)
    await callback.message.answer("Спробуй ввести назву вправи ще раз.")
    await callback.answer()


@router.callback_query(WorkoutFlow.confirm_rir, F.data.startswith("rir:"))
async def handle_rir(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    rir = int(callback.data.split(":")[1])
    data = await state.get_data()
    parsed = _deserialize_parsed(data[_PARSED_KEY])
    canonical_name = data[_RESOLVED_KEY]

    exercise = await _get_exercise_by_name(db, canonical_name)
    if exercise is None:
        await callback.message.answer("⚠️ Вправу не знайдено в базі.")
        await callback.answer()
        return

    workout_session = await get_active_session(db, callback.from_user.id)
    if workout_session is None:
        await callback.message.answer("⚠️ Немає активного тренування.")
        await callback.answer()
        return

    from models.set import ExerciseSet

    for s in parsed:
        db.add(
            ExerciseSet(
                session_id=workout_session.id,
                exercise_id=exercise.id,
                raw_input=canonical_name,
                weight=s["weight"],
                reps=s["reps"],
                rir=rir,
                is_failure=(rir == 0),
            )
        )
    await db.commit()

    await state.set_state(WorkoutFlow.active)
    await callback.message.answer(
        f"💾 Збережено: <b>{canonical_name}</b>\n{_format_sets_preview_raw(parsed)}",
        parse_mode="HTML",
        reply_markup=workout_menu(),
    )
    await callback.answer()


async def _get_exercise_by_name(db: AsyncSession, name: str):
    from models.exercise import Exercise
    from sqlalchemy import select

    result = await db.execute(select(Exercise).where(Exercise.name_uk == name))
    return result.scalar_one_or_none()


def _serialize_parsed(parsed) -> list[dict]:
    return [{"weight": s.weight, "reps": s.reps, "is_failure": s.is_failure} for s in parsed.sets]


def _deserialize_parsed(data: list[dict]) -> list[dict]:
    return data


def _format_sets_preview(parsed) -> str:
    lines = [f"  {s.weight} кг × {s.reps} повт." for s in parsed.sets]
    return "\n".join(lines)


def _format_sets_preview_raw(sets: list[dict]) -> str:
    lines = [f"  {s['weight']} кг × {s['reps']} повт." for s in sets]
    return "\n".join(lines)
