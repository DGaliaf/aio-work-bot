import random

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.keyboards import debank_inline_keyboard, debank_leave_inline_keyboard
from src.services.checkers.debank.debank import Debank
from src.states import DeBank
from src.utils import is_wallet

router: Router = Router()

@router.callback_query(lambda c: c.data == 'debank_checker')
async def debank_checker(callback: types.CallbackQuery):
    checkers_msg = "Добро пожаловать в <b>DeBank чекер</b>\n\nВыберите режим работы:"

    await callback.message.edit_text(text=checkers_msg, reply_markup=debank_inline_keyboard)


@router.callback_query(lambda c: c.data == 'debank_single_parse')
async def debank_single_parse(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DeBank.wallet)

    msg = ("<b>Одиночный режим DeBank</b>\n\nОтправь кошелек и получи баланс!\nЧтобы выйти из этого режима "
           "нажмите - <b>'Выйти</b>'")

    debank = Debank()

    callback_message = await callback.message.answer(text="Отправьте адрес кошелька")
    await state.set_data({"msg_id": callback_message.message_id, "debank": debank})

    await callback.message.edit_text(text=msg, reply_markup=debank_leave_inline_keyboard)


@router.message(DeBank.wallet)
async def check_single_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()

    debank: Debank = data.get("debank")

    await message.delete()

    if not is_wallet(message.text):
        await message.bot.edit_message_text(text=f"Проверьте правильность адреса - {message.text}", chat_id=message.chat.id, message_id=data.get("msg_id"))
    else:
        response = await debank.api("GET", "/user", {"query": {"id": message.text.strip()}})

        user_data = response.get("user")
        balance = user_data.get("stats").get("usd_value")

        if balance is None:
            balance = user_data.get("desc").get("usd_value")

        balance = round(balance)

        await message.bot.edit_message_text(text=f"Баланс адреса {message.text} - ${balance}", chat_id=message.chat.id, message_id=data.get("msg_id"))


@router.callback_query(lambda c: c.data == 'debank_leave')
async def debank_single_parse(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.bot.delete_message(callback.message.chat.id, data.get("msg_id"))

    checkers_msg = "Добро пожаловать в <b>DeBank чекер</b>\n\nВыберите режим работы:"

    await state.clear()
    await callback.message.edit_text(text=checkers_msg, reply_markup=debank_inline_keyboard)
