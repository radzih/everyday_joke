from dataclasses import dataclass
from os import environ


@dataclass
class Database:
    host: str
    port: int
    user: str
    name: str
    password: str


def load_config() -> Database:
    return Database(
        host=environ["DB_HOST"],
        port=int(environ["DB_PORT"]),
        user=environ["DB_USER"],
        name=environ["DB_NAME"],
        password=environ["DB_PASSWORD"],
    )
