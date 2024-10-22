from aiogram import Router
from aiogram.types import Message

from src.keyboards import main_keyboard

router: Router = Router()


@router.message()
async def welcome_message(message: Message):
    welcome_msg = f"Добро пожаловать в рай скамера"

    await message.reply(text=welcome_msg, reply_markup=main_keyboard)
