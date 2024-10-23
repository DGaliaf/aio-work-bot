from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards import main_keyboard_inline

router: Router = Router()


@router.message(CommandStart())
async def welcome(message: Message):
    welcome_msg = "Добро пожаловать в <b>All in One бота</b>\n\n Made by <code>DGaliaf (@dkhodos)</code>"

    await message.reply(text=welcome_msg, reply_markup=main_keyboard_inline)