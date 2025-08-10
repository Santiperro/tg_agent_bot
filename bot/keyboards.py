from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.texts import (
    INFO_BUTTON,
    MANAGE_MEMORY_BUTTON,
    SHOW_STATISTICS_BUTTON,
    CONFIRM_BUTTON,
    CANCEL_BUTTON,
)


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CONFIRM_BUTTON, callback_data="confirm")],
            [InlineKeyboardButton(text=CANCEL_BUTTON, callback_data="cancel")],
        ]
    )


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=INFO_BUTTON, callback_data="menu:info")
    kb.row(
        InlineKeyboardButton(
            text=MANAGE_MEMORY_BUTTON, callback_data="menu:manage_memory"
        ),
        InlineKeyboardButton(
            text=SHOW_STATISTICS_BUTTON, callback_data="menu:stats:page=1"
        ),
    )
    return kb.as_markup()


def back_to_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="menu:main")]]
    )


def manage_memory_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Список записей", callback_data="menu:mem:list:page=1"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Добавить запись", callback_data="menu:mem:add"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Очистить контекст", callback_data="menu:mem:clear_ctx"
                )
            ],
            [InlineKeyboardButton(text="Назад", callback_data="menu:main")],
        ]
    )


def stats_kb(page: int, has_prev: bool, has_next: bool) -> InlineKeyboardMarkup:
    row = []
    if has_prev:
        row.append(
            InlineKeyboardButton(
                text="Назад", callback_data=f"menu:stats:page={page - 1}"
            )
        )
    if has_next:
        row.append(
            InlineKeyboardButton(
                text="Далее", callback_data=f"menu:stats:page={page + 1}"
            )
        )
    inline_keyboard = []
    if row:
        inline_keyboard.append(row)
    inline_keyboard.append(
        [InlineKeyboardButton(text="В меню", callback_data="menu:main")]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
