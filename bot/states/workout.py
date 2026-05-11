from aiogram.fsm.state import State, StatesGroup


class WorkoutFlow(StatesGroup):
    active = State()
    confirm_rir = State()
    confirm_exercise = State()
    select_angle = State()
    confirm_finish = State()
