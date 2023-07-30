from aio_pika import Connection
from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .infra import InfrastructureMiddleware


def setup_middlewares(
    dp: Dispatcher,
    session_factory: async_sessionmaker[AsyncSession],
    ampq_connection: Connection,
):
    dp.update.outer_middleware(
        InfrastructureMiddleware(session_factory, ampq_connection)
    )
