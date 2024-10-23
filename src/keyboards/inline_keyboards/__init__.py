from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from config import get_config, Config

__config: Config = get_config()

parsers_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"{parser_name}", callback_data=f"{parser_name.lower()}_parser")] for parser_name in __config.available_parsers
    ],
    resize_keyboard=True
)
parsers_inline_keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"Назад", callback_data=f"to_main_page")])

checkers_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"{checker_name}", callback_data=f"{checker_name.lower()}_parser")] for checker_name in __config.available_checkers
    ],
    resize_keyboard=True
)
checkers_inline_keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"Назад", callback_data=f"to_main_page")])

base_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"Назад", callback_data=f"to_main_page")]
    ],
    resize_keyboard=True
)

main_keyboard_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Парсеры", callback_data="parsers"),InlineKeyboardButton(text="Чекеры", callback_data="checkers")],
        [InlineKeyboardButton(text="Информация", callback_data="info")],
    ],
    resize_keyboard=True
)