import discord
import os

from core.validate import Validate
from core.bot import Bot
from core.database import Database

from services.clan import CoCService
from dotenv import load_dotenv


async def start(db: Database):
    coc_service = CoCService(db)
    await coc_service.login()
    return coc_service


async def main():
    load_dotenv()
    BOT_KEY = os.getenv("BOT_KEY")
    assert BOT_KEY is not None

    db = Database("database.db")

    intents = discord.Intents.default()
    intents.message_content = True

    service = await start(db)

    client = Bot(
        command_prefix="!",
        service=service,
        validator=Validate(db),
        intents=intents,
    )
    await client.start(BOT_KEY)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
