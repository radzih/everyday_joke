from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from everyday_joke.bot import locales
from everyday_joke.bot.keyboards import button
from everyday_joke.bot.services.commands import set_commands
from everyday_joke.business.user import CreateUser, UserCreateDTO

router = Router()


@router.message(CommandStart(), F.from_user.as_("user"))
async def start_message(
    message: Message, user: User, create_user: CreateUser, bot: Bot
) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(button.subscribe(locales.en.SUBSCRIBE_BUTTON))

    await set_commands(bot=bot, user_id=user.id)
    await create_user(UserCreateDTO(id=user.id, name=user.full_name))

    await message.answer(
        text=locales.en.START_MESSAGE, reply_markup=builder.as_markup()
    )
