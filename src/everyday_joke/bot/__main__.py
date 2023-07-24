from logging import DEBUG, INFO, basicConfig
from aiogram import Dispatcher, Bot

from everyday_joke.config import load_config
from everyday_joke.bot.handlers.setup import include_routers
from everyday_joke.bot.middlewares.setup import setup_middlewares
from everyday_joke.infra.db.main import (
    create_connection_url,
    create_session_factory
)


def configure_logging(debug: bool) -> None:
    basicConfig(level=DEBUG if debug else INFO)


async def main() -> None:
    config = load_config()

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()

    connection_url = create_connection_url(config.db, async_=True)
    session_factory = create_session_factory(connection_url)

    configure_logging(config.debug)
    include_routers(dp)
    setup_middlewares(dp, session_factory)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())