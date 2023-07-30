from dataclasses import dataclass

from everyday_joke.bot.config import TgBot
from everyday_joke.bot.config import load_config as load_bot_config
from everyday_joke.infra.db.config import Database
from everyday_joke.infra.db.config import load_config as load_db_config
from everyday_joke.infra.rabbitmq.config import RabbitMQ
from everyday_joke.infra.rabbitmq.config import \
    load_config as load_rabbitmq_config


@dataclass
class Config:
    tg_bot: TgBot
    db: Database
    rabbitmq: RabbitMQ
    debug: bool = False


def load_config():
    return Config(
        tg_bot=load_bot_config(),
        db=load_db_config(),
        rabbitmq=load_rabbitmq_config(),
        debug=True,
    )
