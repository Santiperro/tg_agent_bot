import logging
from aiogram import BaseMiddleware
from aiogram.types import Message

from config import settings

logger = logging.getLogger(__name__)


class UserFilterMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data: dict):
        if not settings.security_config.enable_chat_whitelist:
            return await handler(event, data)
        
        if event.from_user.id not in settings.security_config.allowed_user_ids:
            logger.info(f"Blocked message from unauthorized user: {event.from_user.id}")
            return
        
        return await handler(event, data) 