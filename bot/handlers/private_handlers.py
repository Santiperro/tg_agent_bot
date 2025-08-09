from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.texts import *
from bot.keyboards import main_inline_keyboard


private_router = Router()

@private_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        text=START_TEXT,
        reply_markup=main_inline_keyboard
)

# Start of Selection
@private_router.message()
async def handle_text_message(message: Message):
    await message.answer("Получил ваше сообщение")
