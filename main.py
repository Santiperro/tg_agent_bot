import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import settings


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


async def main():
    bot = Bot(token=settings.tg_api_config)

    dp = Dispatcher()
    
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())