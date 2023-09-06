from teletdd import TelegramTestClient

from everyday_joke.bot.services.commands import start
from everyday_joke.infra.db.main import DBGateway


async def test_subsribe_start(
    db_gateway: DBGateway, client: TelegramTestClient
) -> None:
    await client.send_message("/" + start.command)
    messages = await client.get_response_messages()
    message = messages[0]
    await client.click_inline_button(message.id, 0)

    user = await db_gateway.get_user((await client.get_me()).id)

    assert user.subscribed is True
