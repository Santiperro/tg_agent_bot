import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.middlewares.user_filter import UserFilterMiddleware
from config import settings
from bot.handlers.private_handlers import private_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


async def main():
    bot = Bot(token=settings.tg_api_token)

    dp = Dispatcher()
    dp.message.middleware(UserFilterMiddleware())
    
    dp.include_router(private_router)
    await dp.start_polling(bot, drop_pending_updates=True)
    
    
if __name__ == '__main__':
    asyncio.run(main())