# [InlineKeyboardButton(text=f"Одиночный режим", callback_data=f"debank_single_parse")],
#         [InlineKeyboardButton(text=f"Файловый режим", callback_data=f"debank_multiple_parse")],
from aiogram import Router, types

from src.keyboards import debank_inline_keyboard, debank_leave_inline_keyboard

router: Router = Router()


@router.callback_query(lambda c: c.data == 'debank_checker')
async def debank_checker(callback: types.CallbackQuery):
    checkers_msg = "Добро пожаловать в <b>DeBank чекер</b>\n\nВыберите режим работы:"

    await callback.message.edit_text(text=checkers_msg, reply_markup=debank_inline_keyboard)

@router.callback_query(lambda c: c.data == 'debank_single_parse')
async def debank_single_parse(callback: types.CallbackQuery):
    msg = ("<b>Одиночный режим DeBank</b>\n\nОтправь кошелек и получу баланс!\nЧтобы выйти из этого режима "
                    "нажмите - <b>'Выйти</b>'")

    await callback.message.edit_text(text=msg, reply_markup=debank_leave_inline_keyboard)

@router.callback_query(lambda c: c.data == 'debank_leave')
async def debank_single_parse(callback: types.CallbackQuery):
    checkers_msg = "Добро пожаловать в <b>DeBank чекер</b>\n\nВыберите режим работы:"

    await callback.message.edit_text(text=checkers_msg, reply_markup=debank_inline_keyboard)