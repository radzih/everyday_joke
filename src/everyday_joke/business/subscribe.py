from enum import Enum

from everyday_joke.infra.db.main import DBGateway
from everyday_joke.infra.rabbitmq.main import RabbitMQAdapter

from .base import Interactor
from .exceptions.user import UserNotFound


class SubscribeResult(Enum):
    subscribed = "subscribed"
    already_subscribed = "already_subscribed"


class SubscribeUser(Interactor):
    def __init__(self, db: DBGateway, rabbitmq: RabbitMQAdapter):
        self.db = db
        self.rabbitmq = rabbitmq

    async def __call__(self, user_id: int) -> SubscribeResult:
        user = await self.db.get_user(user_id=user_id)

        if not user:
            raise UserNotFound(user_id=user_id, on_process=type(self))

        user = await self.db.get_user(user_id=user_id)

        if user.subscribed:
            return SubscribeResult.already_subscribed

        await self.db.subscribe_user(user_id=user_id)
        await self.db.commit()

        await self.rabbitmq.subscribe_user(user_id=user.id)

        return SubscribeResult.subscribed
