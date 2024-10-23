from aiogram import Router, F, types
from aiogram.types import Message

from config import get_config, Config
from src.keyboards import parsers_inline_keyboard, main_keyboard_inline

router: Router = Router()

__config: Config = get_config()


@router.callback_query(lambda c: c.data == 'parsers')
async def parsers(callback: types.CallbackQuery):
    parsers_msg = "<b>Доступные парсеры:</b>"
    for available_parser in __config.available_parsers:
        parsers_msg += f"\n -{available_parser}"

    await callback.message.edit_text(text=parsers_msg, reply_markup=parsers_inline_keyboard)


@router.callback_query(lambda c: c.data == 'to_main_page')
async def go_to_main(callback: types.CallbackQuery):
    welcome_msg = "Добро пожаловать в <b>All in One бота</b>\n\n Made by <code>DGaliaf (@dkhodos)</code>"

    await callback.message.edit_text(text=welcome_msg, reply_markup=main_keyboard_inline)
