from teletdd import TelegramTestClient

from everyday_joke.bot.services.commands import start, subscribe
from everyday_joke.infra.db.main import DBGateway
from everyday_joke.bot import locales


async def test_subsribe_start(
    db_gateway: DBGateway, client: TelegramTestClient
) -> None:
    await client.send_message("/" + start.command)
    messages = await client.get_response_messages()
    message = messages[0]
    await client.click_inline_button(message.id, 0)

    user = await db_gateway.get_user((await client.get_me()).id)

    assert user.subscribed is True
    assert message.text == locales.en.START_MESSAGE


async def test_subscribe_command(
    db_gateway: DBGateway, client: TelegramTestClient
) -> None:
    await client.send_message("/" + subscribe.command)
    messages = await client.get_response_messages()
    message = messages[0]

    user = await db_gateway.get_user((await client.get_me()).id)

    assert user.subscribed is True
    assert message.text == locales.en.SUBSCRIBE_SUCCESS
