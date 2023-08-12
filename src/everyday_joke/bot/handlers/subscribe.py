from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, User

from everyday_joke.bot import locales
from everyday_joke.bot.keyboards import callback
from everyday_joke.business.subscribe import SubscribeResult, SubscribeUser

router = Router()


@router.callback_query(
    callback.Subscribe.filter(),
    F.from_user.as_("user"),
    F.message.as_("message"),
)
async def subscribe(
    call: CallbackQuery,
    message: Message,
    user: User,
    subscribe_user: SubscribeUser,
) -> None:
    result = await subscribe_user(user.id)

    if result == SubscribeResult.subscribed:
        text = locales.en.SUBSCRIBE_SUCCESS
    elif result == SubscribeResult.already_subscribed:
        text = locales.en.ALREADY_SUBSCRIBED

    await call.answer(
        text=text,
        show_alert=True,
    )
    await message.delete()
