from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main import (
    BTN_FINISH_WORKOUT,
    BTN_START_WORKOUT,
    angle_keyboard,
    confirm_exercise_keyboard,
    confirm_finish_keyboard,
    main_menu,
    rir_keyboard,
    workout_menu,
)
from bot.states.workout import WorkoutFlow
from services.exercise_parser import ParseError, parse_exercise_input
from services.exercise_resolver import is_trash, resolve_exercise
from services.workout import finish_session, get_active_session, start_session

router = Router()

_PARSED_KEY = "parsed_input"
_RESOLVED_KEY = "resolved_name"

FORMAT_HINT = (
    "Формат вводу:\n"
    "<code>Назва вправи\n"
    "вага повтори\n"
    "вага повтори</code>\n\n"
    "Наприклад:\n"
    "<code>Жим лежачи\n"
    "100 8\n"
    "100 8\n"
    "95 6</code>\n\n"
    "Вага — кілограми (можна з крапкою: 102.5)\n"
    "Повтори — ціле число\n"
    "Опціонально: додай <code>відказ</code> після повторів якщо був відказ"
)


async def _load_candidates(db: AsyncSession) -> list[tuple[str, list[str]]]:
    from sqlalchemy import select

    from models.exercise import Exercise

    result = await db.execute(select(Exercise))
    exercises = result.scalars().all()
    return [(ex.name_uk, [a.alias for a in ex.aliases]) for ex in exercises]


async def _get_exercise_by_name(db: AsyncSession, name: str):
    from sqlalchemy import select

    from models.exercise import Exercise

    result = await db.execute(select(Exercise).where(Exercise.name_uk == name))
    return result.scalar_one_or_none()


def _serialize_parsed(parsed) -> list[dict]:
    return [{"weight": s.weight, "reps": s.reps, "is_failure": s.is_failure} for s in parsed.sets]


def _format_sets(sets: list[dict]) -> str:
    return "\n".join(f"  {s['weight']} кг × {s['reps']} повт." for s in sets)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    if current is None:
        await message.answer("Немає активної дії для скасування.")
        return
    await state.set_state(WorkoutFlow.active)
    await message.answer("❌ Скасовано. Продовжуй вводити вправи.", reply_markup=workout_menu())


@router.message(F.text == BTN_START_WORKOUT)
async def start_workout(message: Message, state: FSMContext, db: AsyncSession) -> None:
    await start_session(db, message.from_user.id)
    await state.set_state(WorkoutFlow.active)
    await message.answer(
        "💪 Тренування розпочато!\n\n" + FORMAT_HINT,
        parse_mode="HTML",
        reply_markup=workout_menu(),
    )


@router.message(WorkoutFlow.active, F.text == BTN_FINISH_WORKOUT)
async def ask_finish(message: Message, state: FSMContext) -> None:
    await state.set_state(WorkoutFlow.confirm_finish)
    await message.answer("Завершити тренування?", reply_markup=confirm_finish_keyboard())


@router.callback_query(WorkoutFlow.confirm_finish, F.data == "finish:confirm")
async def finish_workout(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    await finish_session(db, callback.from_user.id)
    await state.clear()
    await callback.message.answer("✅ Тренування завершено! Гарна робота 💪", reply_markup=main_menu())
    await callback.answer()


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
        await message.answer(f"⚠️ {e}\n\n{FORMAT_HINT}", parse_mode="HTML")
        return

    if is_trash(parsed.exercise_name):
        await message.answer(f"⚠️ Назва вправи виглядає некоректно.\n\n{FORMAT_HINT}", parse_mode="HTML")
        return

    candidates = await _load_candidates(db)
    result = resolve_exercise(parsed.exercise_name, candidates)

    if result is None:
        await message.answer(
            f"❓ Не вдалось знайти вправу «{parsed.exercise_name}».\n"
            "Перевір назву або спробуй іншу. Введи /cancel щоб скасувати."
        )
        return

    await state.update_data(**{_PARSED_KEY: _serialize_parsed(parsed), _RESOLVED_KEY: result.canonical_name})

    if not result.is_exact:
        await state.set_state(WorkoutFlow.confirm_exercise)
        await message.answer(
            f"🤔 Можливо, маєш на увазі <b>{result.canonical_name}</b>?",
            parse_mode="HTML",
            reply_markup=confirm_exercise_keyboard(result.canonical_name),
        )
        return

    await _after_exercise_confirmed(message, state, db, result.canonical_name)


@router.callback_query(WorkoutFlow.confirm_exercise, F.data == "exercise:confirm")
async def confirmed_exercise(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    data = await state.get_data()
    await _after_exercise_confirmed(callback.message, state, db, data[_RESOLVED_KEY])
    await callback.answer()


@router.callback_query(WorkoutFlow.confirm_exercise, F.data == "exercise:reject")
async def rejected_exercise(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(WorkoutFlow.active)
    await callback.message.answer("Спробуй ввести назву вправи ще раз. Введи /cancel щоб скасувати.")
    await callback.answer()


async def _after_exercise_confirmed(message: Message, state: FSMContext, db: AsyncSession, canonical: str) -> None:
    exercise = await _get_exercise_by_name(db, canonical)
    data = await state.get_data()
    sets = data[_PARSED_KEY]

    if exercise and exercise.has_angle_variant:
        await state.set_state(WorkoutFlow.select_angle)
        await message.answer(
            f"✅ <b>{canonical}</b>\n{_format_sets(sets)}\n\nЯкий кут нахилу?",
            parse_mode="HTML",
            reply_markup=angle_keyboard(),
        )
    else:
        await state.set_state(WorkoutFlow.confirm_rir)
        await message.answer(
            f"✅ <b>{canonical}</b>\n{_format_sets(sets)}\n\nЯк відчувались підходи?",
            parse_mode="HTML",
            reply_markup=rir_keyboard(),
        )


@router.callback_query(WorkoutFlow.select_angle, F.data.startswith("angle:"))
async def handle_angle(callback: CallbackQuery, state: FSMContext) -> None:
    angle = int(callback.data.split(":")[1])
    data = await state.get_data()
    full_name = f"{data[_RESOLVED_KEY]} {angle}°"

    await state.update_data(**{_RESOLVED_KEY: full_name})
    await state.set_state(WorkoutFlow.confirm_rir)

    await callback.message.answer(
        f"✅ <b>{full_name}</b>\n{_format_sets(data[_PARSED_KEY])}\n\nЯк відчувались підходи?",
        parse_mode="HTML",
        reply_markup=rir_keyboard(),
    )
    await callback.answer()


@router.callback_query(WorkoutFlow.confirm_rir, F.data.startswith("rir:"))
async def handle_rir(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    rir = int(callback.data.split(":")[1])
    data = await state.get_data()
    sets = data[_PARSED_KEY]
    canonical_name = data[_RESOLVED_KEY]

    workout_session = await get_active_session(db, callback.from_user.id)
    if workout_session is None:
        await callback.message.answer("⚠️ Немає активного тренування.")
        await callback.answer()
        return

    # For angle variants canonical_name has angle suffix; look up by base name first
    base_name = canonical_name.rsplit(" ", 1)[0] if "°" in canonical_name else canonical_name
    exercise = await _get_exercise_by_name(db, base_name) or await _get_exercise_by_name(db, canonical_name)

    if exercise is None:
        await callback.message.answer("⚠️ Вправу не знайдено в базі.")
        await callback.answer()
        return

    from models.set import ExerciseSet

    for s in sets:
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
        f"💾 Збережено: <b>{canonical_name}</b>\n{_format_sets(sets)}",
        parse_mode="HTML",
        reply_markup=workout_menu(),
    )
    await callback.answer()
