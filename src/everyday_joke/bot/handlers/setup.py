from aiogram import Dispatcher

from . import start, subscribe, user


def include_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(subscribe.router)
    dp.include_router(user.router)
