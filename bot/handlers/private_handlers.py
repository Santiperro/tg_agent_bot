from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import os

from bot.texts import *
from bot.keyboards import main_inline_keyboard
from llm.api import get_response
from config import settings
import logging
from utils.prompt_templates import SYSTEM_PROMPT
from bot.exceptions import LLMApiError


logger = logging.getLogger(__name__)

private_router = Router()

def is_private_chat(message: Message) -> bool:
    return message.chat.type == "private"


@private_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        text=START_TEXT,
        reply_markup=main_inline_keyboard
)

@private_router.message(lambda message: message.text and is_private_chat(message))
async def handle_text_message(message: Message):
    """Handle direct LLM communication"""
    try:
        user_text = message.text
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
        
        response = get_response(
            model=settings.llm_api_config.default_model,
            messages=messages,
            max_tokens=settings.llm_api_config.max_tokens,
            temperature=settings.llm_api_config.temperature,
            top_p=settings.llm_api_config.top_p
        )
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Error in handle_text_message: {e}")
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")