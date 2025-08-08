from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup)

from texts import *


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CONFIRM_BUTTON, callback_data="confirm")],
            [InlineKeyboardButton(text=CANCEL_BUTTON, callback_data="cancel")]
        ]
    )


main_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=INFO_BUTTON)],
        [KeyboardButton(text=MANAGE_MEMORY_BUTTON),
        KeyboardButton(text=SHOW_STATISTICS_BUTTON)]],
    resize_keyboard=True,
    input_field_placeholder="")
