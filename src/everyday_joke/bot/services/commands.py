from aiogram import Bot
from aiogram.types import (BotCommand, BotCommandScopeChat,
                           BotCommandScopeDefault)

start = BotCommand(command="/start", description="Start bot")
subscribe = BotCommand(
    command="/subscribe", description="Subscribe to daily jokes"
)

commands = [start, subscribe]


async def set_commands(bot: Bot, user_id: int) -> None:
    await bot.set_my_commands(
        commands, scope=BotCommandScopeChat(chat_id=user_id)
    )
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
