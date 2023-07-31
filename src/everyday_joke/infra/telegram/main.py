from aiogram import Bot

from everyday_joke.bot.config import TgBot


class TelegramAdapter:
    def __init__(self, config: TgBot) -> None:
        self.bot = Bot(token=config.token)

    async def send_message(self, user_id: int, text: str) -> None:
        await self.bot.send_message(user_id, text)

    async def close(self) -> None:
        await self.bot.session.close()
