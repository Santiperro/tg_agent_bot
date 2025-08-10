from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import os

from bot.texts import *
from bot.keyboards import (
    main_menu_kb,
    back_to_main_kb,
    manage_memory_menu_kb,
    stats_kb,
    get_confirmation_keyboard,
)
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
    await message.answer(text=START_TEXT.strip(), reply_markup=main_menu_kb())

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


# Callback query handlers (menu navigation and stubs)

@private_router.callback_query(F.data == "menu:main")
async def menu_main(cb: CallbackQuery):
    logger.info(f"menu_main by user {cb.from_user.id}")
    await cb.message.edit_text(START_TEXT.strip(), reply_markup=main_menu_kb())
    await cb.answer()


@private_router.callback_query(F.data == "menu:info")
async def menu_info(cb: CallbackQuery):
    logger.info(f"menu_info by user {cb.from_user.id}")
    text = (
        "Как пользоваться: отправьте сообщение. Кнопки открывают управление памятью и статистику."
    )
    await cb.message.edit_text(text, reply_markup=back_to_main_kb())
    await cb.answer()


@private_router.callback_query(F.data == "menu:manage_memory")
async def menu_manage_memory(cb: CallbackQuery):
    logger.info(f"menu_manage_memory by user {cb.from_user.id}")
    await cb.message.edit_text("Управление памятью:", reply_markup=manage_memory_menu_kb())
    await cb.answer()


@private_router.callback_query(F.data.regexp(r"^menu:stats:page=(\\d+)$"))
async def menu_stats(cb: CallbackQuery):
    logger.info(f"menu_stats by user {cb.from_user.id}: data={cb.data}")
    page = int(cb.data.split("=")[-1])
    has_prev = page > 1
    has_next = page < 5
    await cb.message.edit_text(
        f"Статистика. Страница {page}.", reply_markup=stats_kb(page, has_prev, has_next)
    )
    await cb.answer()


@private_router.callback_query(F.data == "menu:mem:clear_ctx")
async def mem_clear_confirm(cb: CallbackQuery):
    logger.info(f"mem_clear_confirm by user {cb.from_user.id}")
    await cb.message.edit_text(
        "Очистить контекст? Подтвердите действие.",
        reply_markup=get_confirmation_keyboard(),
    )
    await cb.answer()


@private_router.callback_query(F.data == "confirm")
async def mem_clear_do(cb: CallbackQuery):
    logger.info(f"mem_clear_do by user {cb.from_user.id}")
    # TODO: implement context clearing
    await cb.message.edit_text("Контекст очищен.", reply_markup=manage_memory_menu_kb())
    await cb.answer()


@private_router.callback_query(F.data == "cancel")
async def cancel_action(cb: CallbackQuery):
    logger.info(f"cancel_action by user {cb.from_user.id}")
    await cb.message.edit_text("Действие отменено.", reply_markup=manage_memory_menu_kb())
    await cb.answer()


@private_router.callback_query(F.data.regexp(r"^menu:mem:list:page=(\\d+)$"))
async def mem_list(cb: CallbackQuery):
    logger.info(f"mem_list by user {cb.from_user.id}: data={cb.data}")
    page = int(cb.data.split("=")[-1])
    # TODO: implement memory list retrieval and pagination
    await cb.message.edit_text(
        f"Список записей (заглушка). Страница {page}.",
        reply_markup=manage_memory_menu_kb(),
    )
    await cb.answer()


@private_router.callback_query(F.data == "menu:mem:add")
async def mem_add(cb: CallbackQuery):
    logger.info(f"mem_add by user {cb.from_user.id}")
    # TODO: implement FSM to capture text for new memory entry
    await cb.message.edit_text(
        "Добавление записи (заглушка). Отправьте текст записью обычным сообщением.",
        reply_markup=manage_memory_menu_kb(),
    )
    await cb.answer()