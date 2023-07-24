from aiogram import Router, F
from aiogram.types import Message, User
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from everyday_joke.bot import locales 
from everyday_joke.bot.keyboards import button
from everyday_joke.infra.db.main import DBGateway

router = Router()

async def add_user_to_db(id: int, name: str, db: DBGateway) -> None:
    await db.create_user(name=name, id=id)
    await db.commit()


@router.message(CommandStart(), F.from_user.as_("user"))
async def start_message(message: Message, user: User, db: DBGateway) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(button.subscribe(locales.en.SUBSCRIBE_BUTTON))

    await add_user_to_db(
        id=user.id,
        name=user.full_name,
        db=db,
    )

    await message.answer(
        text=locales.en.START_MESSAGE,
        reply_markup=builder.as_markup()
    )
