import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bot.middlewares.user_filter import UserFilterMiddleware
from config import settings
from bot.handlers.private_handlers import private_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


async def main():
    bot = Bot(token=settings.tg_api_token)
    commands = [
        BotCommand(command="start", description="Открыть главное меню"),
        BotCommand(command="remember", description="Добавить запись в память"),
        BotCommand(command="list_memories", description="Показать записи памяти"),
        BotCommand(command="model_settings", description="Настройки модели"),
        BotCommand(command="clean_context", description="Очистить контекст"),
    ]
    await bot.set_my_commands(commands)

    dp = Dispatcher()
    dp.message.middleware(UserFilterMiddleware())
    
    dp.include_router(private_router)
    await dp.start_polling(bot, drop_pending_updates=True)
    
    
if __name__ == '__main__':
    asyncio.run(main())