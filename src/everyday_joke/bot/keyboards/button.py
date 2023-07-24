from aiogram.types import InlineKeyboardButton

from everyday_joke.bot.keyboards import callback


def subscribe(text: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text, 
        callback_data=callback.Subscribe().pack()
    )
