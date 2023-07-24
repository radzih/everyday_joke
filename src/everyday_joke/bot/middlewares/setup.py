from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .infra import InfrastructureMiddleware


def setup_middlewares(
    dp: Dispatcher, session_factory: async_sessionmaker[AsyncSession]
):
    dp.update.outer_middleware(InfrastructureMiddleware(session_factory))
