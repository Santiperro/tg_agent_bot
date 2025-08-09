from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup)

from bot.texts import *


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CONFIRM_BUTTON, callback_data="confirm")],
            [InlineKeyboardButton(text=CANCEL_BUTTON, callback_data="cancel")]
        ]
    )


main_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=INFO_BUTTON.strip(), callback_data="menu:info")],
        [
            InlineKeyboardButton(text=MANAGE_MEMORY_BUTTON.strip(), callback_data="menu:manage_memory"),
            InlineKeyboardButton(text=SHOW_STATISTICS_BUTTON.strip(), callback_data="menu:stats"),
        ],
    ]
)
