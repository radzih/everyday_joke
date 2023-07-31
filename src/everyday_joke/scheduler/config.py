from dataclasses import dataclass
from os import environ


@dataclass
class Scheduler:
    time: str
    timezone: str


def load_config():
    return Scheduler(
        time=environ["SCHEDULER_TIME"], timezone=environ["SCHEDULER_TIMEZONE"]
    )
