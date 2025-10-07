from discord.ext import commands
from core.database import Database


class Register(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Database("database.db")

    @commands.command(name="register")
    async def register(self, ctx, clan_tag: str):
        await self.client.clan_info.fetch(clan_tag)

        if self.db.get_user(ctx.author.id):
            self.db.update_clan_tag(ctx.author.id, clan_tag)
            await ctx.send("✅ Clan tag updated.")
            return

        self.db.add_user(ctx.author.id, ctx.author.name, clan_tag)

        await ctx.send(
            f"📝 Assigned to {self.client.clan_info.get_clan().name} - {self.client.clan_info.get_clan().tag}"
        )


async def setup(client):
    await client.add_cog(Register(client))
