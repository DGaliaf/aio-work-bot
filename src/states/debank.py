from aiogram.fsm.state import StatesGroup, State


class DeBank(StatesGroup):
    wallet = State()
    # proceed_wallet = State()