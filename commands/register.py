import discord

from discord.ext import commands

from core.database import Database
from core.bot import Bot


class Register(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client
        self.db = Database("database.db")

    @commands.command(name="register")
    async def register(self, ctx: commands.Context, clan_tag: str):
        if not ctx.guild:
            await ctx.send("⛔ This command can only be used in a server.")
            return

        member = ctx.author
        if not isinstance(member, discord.Member):
            try:
                member = await ctx.guild.fetch_member(ctx.author.id)
            except discord.NotFound:
                await ctx.send("⛔ Unable to verify your permissions.")
                return
            except discord.HTTPException:
                await ctx.send("⛔ An error occurred while verifying your permissions.")
                return

        if not member.guild_permissions.administrator:
            await ctx.send("⛔ You need to be an administrator to use this command.")
            return

        if self.db.get_server(ctx.guild.id):
            self.db.update_clan_tag(ctx.guild.id, clan_tag)
            await ctx.send("✅ Clan tag updated.")
            return

        self.db.add_server(ctx.guild.id, clan_tag)

        clan = await self.client.service.get_clan(ctx.guild.id)
        if not clan:
            await ctx.send(
                "⛔ Clan not found. Please check the clan tag and try again."
            )
            return

        await ctx.send(f"📝 Assigned to {clan.name} - {clan.tag}")


async def setup(client):
    await client.add_cog(Register(client))
