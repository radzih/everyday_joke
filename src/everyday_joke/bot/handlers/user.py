from aiogram import Bot, F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import CallbackQuery, ErrorEvent, Message

from everyday_joke.bot.handlers.subscribe import (
    subscribe_call,
    subscribe_command,
)
from everyday_joke.business.exceptions.user import UserNotFound
from everyday_joke.business.subscribe import SubscribeUser
from everyday_joke.business.user import CreateUser, UserCreateDTO

router = Router(name="error")


@router.errors(
    ExceptionTypeFilter(UserNotFound),
    F.exception.as_("exception"),
    F.update.callback_query.as_("call"),
    F.update.callback_query.message.as_("message"),
)
async def user_not_found_call(
    event: ErrorEvent,
    call: CallbackQuery,
    message: Message,
    exception: UserNotFound,
    bot: Bot,
    create_user: CreateUser,
    subscribe_user: SubscribeUser,
) -> None:
    user_id = exception.user_id
    interactor = exception.on_process

    chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    user = chat_member.user

    await create_user(UserCreateDTO(id=user.id, name=user.full_name))

    if interactor is SubscribeUser:
        await subscribe_call(call, message, user, subscribe_user)


@router.errors(
    ExceptionTypeFilter(UserNotFound),
    F.exception.as_("exception"),
    F.update.message.as_("message"),
)
async def user_not_found_message(
    event: ErrorEvent,
    message: Message,
    exception: UserNotFound,
    bot: Bot,
    create_user: CreateUser,
    subscribe_user: SubscribeUser,
) -> None:
    user = await get_and_create_user(exception, bot)

    await create_user(UserCreateDTO(id=user.id, name=user.full_name))

    if exception.on_process is SubscribeUser:
        await subscribe_command(message, user, subscribe_user)


async def get_and_create_user(exception: UserNotFound, bot: Bot):
    user_id = exception.user_id

    chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    user = chat_member.user
    return user
