from aiogram import Router, types
from config import get_config, Config
from src.keyboards import main_keyboard_inline, checkers_inline_keyboard

router: Router = Router()

__config: Config = get_config()


@router.callback_query(lambda c: c.data == 'checkers')
async def checkers(callback: types.CallbackQuery):
    checkers_msg = "<b>Доступные чекеры:</b>"
    for available_checker in __config.available_checkers:
        checkers_msg += f"\n -{available_checker}"

    await callback.message.edit_text(text=checkers_msg, reply_markup=checkers_inline_keyboard)


@router.callback_query(lambda c: c.data == 'to_checkers')
async def go_to_main(callback: types.CallbackQuery):
    checkers_msg = "<b>Доступные чекеры:</b>"
    for available_checker in __config.available_checkers:
        checkers_msg += f"\n -{available_checker}"

    await callback.message.edit_text(text=checkers_msg, reply_markup=checkers_inline_keyboard)


@router.callback_query(lambda c: c.data == 'to_main_page')
async def go_to_main(callback: types.CallbackQuery):
    welcome_msg = "Добро пожаловать в <b>All in One бота</b>\n\n Made by <code>DGaliaf (@dkhodos)</code>"

    await callback.message.edit_text(text=welcome_msg, reply_markup=main_keyboard_inline)
