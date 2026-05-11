from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

BTN_START_WORKOUT = "🏋️ Почати тренування"
BTN_FINISH_WORKOUT = "✅ Завершити тренування"
BTN_CANCEL = "❌ Скасувати"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_START_WORKOUT)]],
        resize_keyboard=True,
    )


def workout_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_FINISH_WORKOUT)]],
        resize_keyboard=True,
        input_field_placeholder="Назва вправи + підходи...",
    )


def rir_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="😅 Відказ (RIR 0)", callback_data="rir:0")
    builder.button(text="💪 Важко (RIR 1)", callback_data="rir:1")
    builder.button(text="👌 Норм (RIR 2)", callback_data="rir:2")
    builder.button(text="😊 Легко (RIR 3+)", callback_data="rir:3")
    builder.adjust(2)
    return builder.as_markup()


def confirm_exercise_keyboard(canonical_name: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"✅ Так, {canonical_name}", callback_data="exercise:confirm")
    builder.button(text="❌ Ні, інша вправа", callback_data="exercise:reject")
    builder.adjust(1)
    return builder.as_markup()


STANDARD_ANGLES = [15, 30, 45, 60, 75]


def angle_keyboard():
    builder = InlineKeyboardBuilder()
    for angle in STANDARD_ANGLES:
        builder.button(text=f"{angle}°", callback_data=f"angle:{angle}")
    builder.adjust(5)
    return builder.as_markup()


def confirm_finish_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Завершити", callback_data="finish:confirm")
    builder.button(text="↩️ Продовжити", callback_data="finish:cancel")
    builder.adjust(2)
    return builder.as_markup()
