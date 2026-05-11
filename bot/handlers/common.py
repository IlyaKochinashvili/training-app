from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.profile import start_onboarding
from bot.keyboards.main import BTN_START_WORKOUT, main_menu
from services.user_profile import get_profile

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()

    profile = await get_profile(db, message.from_user.id)
    if not profile:
        await start_onboarding(message, state)
        return

    await message.answer(
        f"Привіт! Я допоможу відстежувати твої тренування та прогресію.\n\nНатисни «{BTN_START_WORKOUT}», щоб почати.",
        reply_markup=main_menu(),
    )
