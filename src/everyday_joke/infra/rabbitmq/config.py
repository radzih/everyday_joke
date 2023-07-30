from dataclasses import dataclass
from os import environ


@dataclass
class RabbitMQ:
    port: int
    host: str
    username: str
    password: str


def load_config() -> RabbitMQ:
    return RabbitMQ(
        host=environ["RABBITMQ_HOST"],
        port=environ["RABBITMQ_PORT"],
        username=environ["RABBITMQ_USER"],
        password=environ["RABBITMQ_PASS"],
    )
