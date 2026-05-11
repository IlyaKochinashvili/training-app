from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main import main_menu
from bot.states.onboarding import Onboarding
from models.user_profile import Sex
from services.user_profile import create_profile, get_profile

router = Router()

SEX_LABELS = {Sex.male: "🙋 Чоловік", Sex.female: "🙋‍♀️ Жінка"}


def _sex_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text=SEX_LABELS[Sex.male], callback_data="sex:male")
    builder.button(text=SEX_LABELS[Sex.female], callback_data="sex:female")
    builder.adjust(2)
    return builder.as_markup()


async def start_onboarding(message: Message, state: FSMContext) -> None:
    await state.set_state(Onboarding.height)
    await message.answer(
        "Привіт! Спершу налаштуємо твій профіль — це потрібно для точних рекомендацій.\n\nВведи свій зріст (см):"
    )


@router.message(Onboarding.height)
async def handle_height(message: Message, state: FSMContext) -> None:
    try:
        height = int(message.text.strip())
        if not (100 <= height <= 250):
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введи коректний зріст від 100 до 250 см:")
        return

    await state.update_data(height_cm=height)
    await state.set_state(Onboarding.weight)
    await message.answer("Введи свою вагу (кг):")


@router.message(Onboarding.weight)
async def handle_weight(message: Message, state: FSMContext) -> None:
    try:
        weight = float(message.text.strip().replace(",", "."))
        if not (30.0 <= weight <= 300.0):
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введи коректну вагу від 30 до 300 кг:")
        return

    await state.update_data(weight_kg=weight)
    await state.set_state(Onboarding.age)
    await message.answer("Скільки тобі років?")


@router.message(Onboarding.age)
async def handle_age(message: Message, state: FSMContext) -> None:
    try:
        age = int(message.text.strip())
        if not (10 <= age <= 100):
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введи коректний вік від 10 до 100:")
        return

    await state.update_data(age=age)
    await state.set_state(Onboarding.sex)
    await message.answer("Стать:", reply_markup=_sex_keyboard())


@router.callback_query(Onboarding.sex, F.data.startswith("sex:"))
async def handle_sex(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    sex = Sex(callback.data.split(":")[1])
    data = await state.get_data()

    await create_profile(
        db,
        user_id=callback.from_user.id,
        height_cm=data["height_cm"],
        weight_kg=data["weight_kg"],
        age=data["age"],
        sex=sex,
    )

    await state.clear()
    await callback.message.answer(
        "✅ Профіль збережено! Тепер можна починати тренування.",
        reply_markup=main_menu(),
    )
    await callback.answer()


@router.message(Command("profile"))
async def cmd_profile(message: Message, db: AsyncSession) -> None:
    profile = await get_profile(db, message.from_user.id)

    if not profile:
        await message.answer("Профіль не знайдено. Введи /start, щоб налаштувати.")
        return

    sex_label = SEX_LABELS.get(profile.sex, profile.sex)
    await message.answer(
        f"👤 <b>Твій профіль</b>\n\n"
        f"Зріст: {profile.height_cm} см\n"
        f"Вага: {profile.weight_kg} кг\n"
        f"Вік: {profile.age} р.\n"
        f"Стать: {sex_label}",
        parse_mode="HTML",
    )
