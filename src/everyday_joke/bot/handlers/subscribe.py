from enum import Enum

from aiogram import F, Router
from aiogram.types import User, CallbackQuery, Message

from everyday_joke.bot import locales
from everyday_joke.bot.keyboards import callback
from everyday_joke.infra.db.main import DBGateway


router = Router()

class SubscribeResult(Enum):
    subscribed = "subscribed"
    already_subscribed = "already_subscribed"

async def subscribe_user(
    user_id: int,
    db: DBGateway
) -> None:
    user = await db.get_user(user_id=user_id)

    if not user:
        await db.create_user(id=user_id)

    user = await db.get_user(user_id=user_id)

    if user.subscribed:
        return SubscribeResult.already_subscribed

    await db.subscribe_user(user_id=user_id)
    await db.commit()

    return SubscribeResult.subscribed


@router.callback_query(
    callback.Subscribe.filter(),
    F.from_user.as_("user"),
    F.message.as_("message")
)
async def subscribe(
    call: CallbackQuery, 
    message: Message,
    user: User,
    db: DBGateway
) -> None:
    result = await subscribe_user(user.id, db)

    if result == SubscribeResult.subscribed:
        text = locales.en.SUBSCRIBE_SUCCESS
    elif result == SubscribeResult.already_subscribed:
        text = locales.en.ALREADY_SUBSCRIBED,

    await call.answer(
        text=text,
        show_alert=True,
    )
    await message.delete()



