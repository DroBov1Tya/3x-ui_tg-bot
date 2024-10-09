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
        
        user_info = await get_user_info(event.chat.id)
        message = event

        if not user_info['Success']:
            text, markup = await bot_logic.start_cmd(message)
            await message.bot.send_message(message.chat.id, text, reply_markup=markup)
            await api.create_user(message)
            return

        if user_info['user']['is_banned']:
            text, markup = await bot_logic.decline(message.chat.id)
            await message.bot.send_message(message.chat.id, text, reply_markup=markup)
            return

        else:
            await handler(message, data)
            return


            # # if message here:
            # if event.text: 
            #     message = event
            #     await handler(message, data)
            #     return
            
            # # if callback button here:
            # elif event:
            #     callbackquery = event
            #     await handler(callbackquery, data)
            #     return
                
            # # if inline mode triggere here:
            # elif event.inline_query:
            #     inlinequery = event
            #     await handler(inlinequery, data)
            #     return
