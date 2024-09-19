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
            # print("You are not in DB!", flush=True)
            await api.create_user(message)
            await message.bot.send_message(message.chat.id, "Ваша заявка на использование бота отправлена администратору")
            admins = await api.admin_fetchadmins()
            user = {
                "User":         message.chat.id,
                "Nickname":     f"@{message.chat.username}",
                "First name":   message.chat.first_name,
                "Last name":    message.chat.last_name ,
            }
            output = str()
            for key, value in user.items():
                output += f"{key}: {value}\n"
            for admin in admins['result']:
                await message.bot.send_message(chat_id=admin, text=f"{output}\nзапрашивает доступ к боту", reply_markup=BTN.admin_add_user(admin, message.chat.id))
            # text, markup = await logic.start_cmd(message)
            # await message.answer(text, reply_markup=markup)
            # send activate BTN to admins

            return

        if user_info['user']['is_banned']:
            print("You are not able to use this bot! (send request to ADMIN)", flush=True)
            await message.bot.send_message(message.chat.id, "Bot offline...")
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
