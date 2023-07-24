import pyjokes
from dataclasses import dataclass

ALL_CATEGORIES = "all"

@dataclass
class Joke:
    text: str


class JokeAdapter:
    async def get_joke(self) -> Joke:
        pyjokes.get_joke(category=ALL_CATEGORIES)

