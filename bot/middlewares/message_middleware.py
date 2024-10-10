from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Update
from config import admins
from modules import bot_logic, api, BTN

async def get_user_info(tgid) -> dict:
    r = await api.user_info(tgid)
    return r

class message_middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], 
        event: Update, 
        data: Dict[str, Any],
    ) -> Any:
        
        message = event
        user_info = await get_user_info(message.chat.id)

        if not user_info['Success']:
            await api.create_user(message)
            text, markup = await bot_logic.start_cmd(message)
            await message.bot.send_message(message.chat.id, text, reply_markup=markup)
            return

        if user_info['user']['is_banned']:
            text, markup = await bot_logic.decline(message.chat.id)
            await message.bot.send_message(message.chat.id, text, reply_markup=markup)
            return

        else:
            await handler(message, data)
            return