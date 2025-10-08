import discord
from core.database import Database
from discord.ext import commands


class Validate:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def server_registered(self, ctx: commands.Context) -> bool:
        guild = self.require_guild(ctx)
        server = self.db.get_server(guild.id)

        if not server:
            await ctx.send(
                "⛔ This server does not have a clan registered.\n 📝 Please use the !register <clan_tag> command."
            )
            return False
        return True

    def require_guild(self, ctx: commands.Context) -> discord.Guild:
        if not ctx.guild:
            raise ValueError("This command can only be used in a server.")
        return ctx.guild
