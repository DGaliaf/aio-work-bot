from aiogram import Router, types
from config import get_config, Config
from src.keyboards import main_keyboard_inline, base_inline_keyboard

router: Router = Router()

__config: Config = get_config()


@router.callback_query(lambda c: c.data == 'info')
async def info(callback: types.CallbackQuery):
    info_msg = "Здесь должна быть информация о проекте, ее создателе, что-то про поддержку и тд. НО ЭТОГО НЕТ :("

    await callback.message.edit_text(text=info_msg, reply_markup=base_inline_keyboard)


@router.callback_query(lambda c: c.data == 'to_main_page')
async def go_to_main(callback: types.CallbackQuery):
    welcome_msg = "Добро пожаловать в <b>All in One бота</b>\n\n Made by <code>DGaliaf (@dkhodos)</code>"

    await callback.message.edit_text(text=welcome_msg, reply_markup=main_keyboard_inline)
