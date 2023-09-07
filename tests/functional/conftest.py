from os import environ
from asyncio import get_event_loop_policy, AbstractEventLoop
from typing import Generator

from _pytest.scope import Scope
from alembic import config as alembic_config
from pytest import fixture
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from teletdd import TelegramTestClient

from everyday_joke.config import Config, load_config
from everyday_joke.infra.db.main import (
    DBGateway,
    create_connection_url,
    create_session_factory,
)


@fixture(scope=Scope.Session)
def config() -> Config:
    return load_config()


@fixture(scope=Scope.Session)
def session_factory(config: Config) -> async_sessionmaker[AsyncSession]:
    connection_url = create_connection_url(config.db, async_=True)
    return create_session_factory(connection_url)


@fixture(scope=Scope.Function)
async def db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> Generator[AsyncSession, None, None]:
    async with session_factory() as session:
        yield session


@fixture(scope=Scope.Function, autouse=True)
async def prepare_db(db_session: AsyncSession) -> Generator:
    alembic_config.main(argv=["upgrade", "head"])

    yield

    schema: str = "public"
    
    await db_session.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE;"))
    await db_session.commit()
    await db_session.execute(text(f"CREATE SCHEMA {schema};"))
    await db_session.commit()


@fixture(scope=Scope.Function)
async def client(config: Config) -> Generator[TelegramTestClient, None, None]:
    client = TelegramTestClient(
        bot_token=config.tg_bot.token,
        api_id=environ["TDLIB_API_ID"],
        api_hash=environ["TDLIB_API_HASH"],
        phone=environ["USERBOT_PHONE"],
        password=environ["USERBOT_PASSWORD"],
    )
    await client.setup()

    yield client

    await client.disconnect()


@fixture(scope=Scope.Function)
async def db_gateway(db_session: AsyncSession) -> DBGateway:
    return DBGateway(db_session)


@fixture(scope=Scope.Session)
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()