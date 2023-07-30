from logging import getLogger

from aio_pika import Connection, Message
from aio_pika.connection import make_url

from everyday_joke.infra.rabbitmq.config import RabbitMQ

SUBSCRIBE_QUEUE = "subscribe"
SUBSCRIBE_ROUTING_KEY = "subscribe"

logger = getLogger(__name__)


def create_amqp_conection(config: RabbitMQ) -> Connection:
    connection_url = make_url(
        login=config.username,
        password=config.password,
        host=config.host,
        port=config.port,
    )
    return Connection(connection_url)


class RabbitMQAdapter:
    def __init__(self, connection: Connection):
        self._connection = connection

    async def connect(self):
        await self._connection.connect()

    async def _publish(self, routing_key: str, body: str) -> None:
        channel = await self._connection.channel()
        await channel.declare_queue(routing_key, durable=True)

        logger.debug(f"Publishing message to {routing_key} queue")

        message = Message(body=body.encode())

        await channel.default_exchange.publish(
            message=message, routing_key=routing_key
        )

    async def subscribe_user(self, user_id: int) -> None:
        await self._publish(SUBSCRIBE_ROUTING_KEY, str(user_id))
