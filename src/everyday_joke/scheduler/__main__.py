import asyncio
import datetime
import logging

import pytz
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from everyday_joke.config import Config, configure_logging, load_config
from everyday_joke.infra.db.main import (
    DBGateway,
    create_connection_url,
    create_session_factory,
)
from everyday_joke.infra.joke.main import JokeAdapter
from everyday_joke.infra.telegram.main import TelegramAdapter

MINUTE = 60  # seconds in minute

logger = logging.getLogger(__name__)


async def task(telegram: TelegramAdapter, joke: JokeAdapter, db: DBGateway):
    users = await db.get_users(is_subscribed=True)

    for user in users:
        joke_ = await joke.get_joke()
        await telegram.send_message(user_id=user.id, text=joke_.text)
        logger.info(f"Sent joke to user {user.id}")


async def scheduler(
    config: Config,
    session_factory: async_sessionmaker[AsyncSession],
    joke: JokeAdapter,
    telegram: TelegramAdapter,
):
    while True:
        await asyncio.sleep(MINUTE)

        tz = pytz.timezone(config.scheduler.timezone)
        curr_time = datetime.datetime.now(tz=tz).strftime("%H:%M")

        if curr_time == config.scheduler.time:
            async with session_factory() as session:
                db = DBGateway(session)
                await task(telegram, joke, db)


async def main():
    config = load_config()
    configure_logging(config.debug)

    connection_url = create_connection_url(config.db, async_=True)
    session_factory = create_session_factory(connection_url)

    joke = JokeAdapter()
    telegram = TelegramAdapter(config.tg_bot)

    logger.error("Scheduler started")
    try:
        await scheduler(config, session_factory, joke, telegram)
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        await telegram.close()


if __name__ == "__main__":
    asyncio.run(main())
    logger.error("Scheduler stopped")
