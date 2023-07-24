from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


@dataclass
class UserDTO:
    id: int
    name: str
    created_date: datetime
    subscribed: bool


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(default=func.now())
    subscribed: Mapped[bool] = mapped_column(default=False)
