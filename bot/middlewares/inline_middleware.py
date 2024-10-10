from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Update
from modules.api import user_info
from modules import bot_logic, api

async def get_user_info(tgid) -> dict:
    r = await user_info(tgid)
    return r

class inline_middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]], 
        event: Update, 
        data: Dict[str, Any],
    ) -> Any:
        
        message = event.message
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
            await handler(event, data)
            return