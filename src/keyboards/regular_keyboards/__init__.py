from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Парсеры"),KeyboardButton(text="Чекеры")],
        [KeyboardButton(text="Информация")],
    ],
    resize_keyboard=True
)