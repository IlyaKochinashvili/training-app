from aiogram.fsm.state import State, StatesGroup


class WorkoutFlow(StatesGroup):
    # Active workout: waiting for exercise input or /finish
    active = State()
    # Received exercise text, waiting for RIR confirmation
    confirm_rir = State()
    # Received low-confidence match, waiting for user to confirm exercise name
    confirm_exercise = State()
    # Waiting for finish confirmation
    confirm_finish = State()
