from typing import Any, Awaitable, Callable, Dict

from aio_pika import Connection
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from everyday_joke.business.subscribe import SubscribeUser
from everyday_joke.business.user import CreateUser
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
        db_session = self.sessionmaker()
        db = DBGateway(db_session)
        rabbitmq = RabbitMQAdapter(self.ampq_connection)

        data["create_user"] = CreateUser(db)
        data["subscribe_user"] = SubscribeUser(db, rabbitmq)

        await handler(event, data)
        await db_session.close()
