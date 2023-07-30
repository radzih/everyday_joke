from aiogram import Bot, Dispatcher

from everyday_joke.bot.handlers.setup import include_routers
from everyday_joke.bot.middlewares.setup import setup_middlewares
from everyday_joke.config import configure_logging, load_config
from everyday_joke.infra.db.main import (create_connection_url,
                                         create_session_factory)
from everyday_joke.infra.rabbitmq.main import create_amqp_conection


async def main() -> None:
    config = load_config()
    configure_logging(config.debug)

    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()

    connection_url = create_connection_url(config.db, async_=True)
    session_factory = create_session_factory(connection_url)

    amqp_connection = create_amqp_conection(config.rabbitmq)
    await amqp_connection.connect()

    include_routers(dp)
    setup_middlewares(dp, session_factory, amqp_connection)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
