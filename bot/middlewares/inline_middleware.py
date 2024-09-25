from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Update
from modules.api import user_info


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
        
        user_info = await get_user_info(event.message.chat.id)

        
        if not user_info['Success']:
            print("You are not in DB!", flush=True)
            # TODO: regme
        
        if user_info['user']['is_banned']:
            print("You are not able to use this bot! (send request to ADMIN)", flush=True)
        
        else:
            await handler(event, data)
        return