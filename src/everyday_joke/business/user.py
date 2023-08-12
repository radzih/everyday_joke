from dataclasses import dataclass

from everyday_joke.infra.db.main import DBGateway

from .base import Interactor


@dataclass
class UserCreateDTO:
    id: int
    name: str


class CreateUser(Interactor):
    def __init__(self, db: DBGateway):
        self.db = db

    async def __call__(self, data: UserCreateDTO) -> bool:
        result = await self.db.create_user(id=data.id, name=data.name)
        await self.db.commit()
        return result
