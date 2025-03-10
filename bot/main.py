import config
import logging
import asyncio
import sys
from modules import handlers
from modules.commands import set_bot_commands
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


TOKEN = config.bot_token
dp = Dispatcher()


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(handlers.router)
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) # logging
    asyncio.run(main())