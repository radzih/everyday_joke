from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, User

from everyday_joke.bot import locales
from everyday_joke.bot.keyboards import callback
from everyday_joke.bot.services import commands
from everyday_joke.business.subscribe import SubscribeResult, SubscribeUser

router = Router()


async def subscribe(
    user_id: int,
    subscribe_user: SubscribeUser,
) -> str:
    result = await subscribe_user(user_id)

    if result == SubscribeResult.subscribed:
        text = locales.en.SUBSCRIBE_SUCCESS
    elif result == SubscribeResult.already_subscribed:
        text = locales.en.ALREADY_SUBSCRIBED

    return text


@router.callback_query(
    callback.Subscribe.filter(),
    F.from_user.as_("user"),
    F.message.as_("message"),
)
async def subscribe_call(
    call: CallbackQuery,
    message: Message,
    user: User,
    subscribe_user: SubscribeUser,
) -> None:
    text = await subscribe(user.id, subscribe_user)

    await call.answer(
        text=text,
        show_alert=True,
    )
    await message.delete()


@router.message(
    Command(commands.subscribe),
    F.from_user.as_("user"),
)
async def subscribe_command(
    message: Message, user: User, subscribe_user: SubscribeUser
) -> None:
    text = await subscribe(user.id, subscribe_user)
    await message.delete()

    await message.answer(text)
