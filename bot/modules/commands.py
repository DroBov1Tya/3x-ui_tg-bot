from aiogram import Bot, types

async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Start interacting with the bot"),
        types.BotCommand(command="/menu", description="Display the menu"),
        types.BotCommand(command="/voucher", description="Activate a voucher"),
        types.BotCommand(command="/help", description="Get help on using the bot")
    ]
    await bot.set_my_commands(commands)
