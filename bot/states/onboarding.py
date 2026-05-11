from aiogram.fsm.state import State, StatesGroup


class Onboarding(StatesGroup):
    height = State()
    weight = State()
    age = State()
    sex = State()
