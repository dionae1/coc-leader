import discord

from discord.ext import commands
from cogwatch import watch

from core.validate import Validate
from services.clan import CoCService


class Bot(commands.Bot):
    def __init__(
        self,
        command_prefix,
        service: CoCService,
        validator: Validate,
        intents: discord.Intents,
    ):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.validator = validator
        self.service = service

    @watch(path="commands", preload=True)
    async def on_ready(self):
        print(f"Bot ready!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.process_commands(message)
