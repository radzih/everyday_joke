from typing import Any, Awaitable, Callable, Dict

from aio_pika import Connection
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from everyday_joke.infra.db.main import DBGateway
from everyday_joke.infra.rabbitmq.main import RabbitMQAdapter


class InfrastructureMiddleware(BaseMiddleware):
    def __init__(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
        ampq_connection: Connection,
    ) -> None:
        self.sessionmaker = sessionmaker
        self.ampq_connection = ampq_connection

    async def __call__(
        self,
        handler: Callable[
            [TelegramObject, Dict[str, Any]],
            Awaitable[Any],
        ],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["rabbitmq"] = RabbitMQAdapter(self.ampq_connection)

        async with self.sessionmaker() as session:
            data["db"] = DBGateway(session)

            await handler(event, data)
