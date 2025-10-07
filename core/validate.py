from core.database import Database
from discord.ext import commands


class Validate:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def user_registered(self, ctx: commands.Context) -> bool:
        user = self.db.get_user(ctx.author.id)
        if not user:
            await ctx.send(
                "⛔ You are not registered.\n 📝 Please use the !register <clan_tag> command."
            )
            return False
        return True
