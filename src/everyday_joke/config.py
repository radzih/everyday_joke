from dataclasses import dataclass

from everyday_joke.bot.config import TgBot, load_config as load_bot_config
from everyday_joke.infra.db.config import (
    Database, 
    load_config as load_db_config
)


@dataclass
class Config:
    tg_bot: TgBot
    db: Database
    debug: bool = False


def load_config():
    return Config(
        tg_bot=load_bot_config(),
        db=load_db_config(),
        debug=True,
    )
        
