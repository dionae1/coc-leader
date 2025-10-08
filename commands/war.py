import coc
import discord

from discord.ext import commands

from core.bot import Bot


class War(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command(name="war")
    async def war(self, ctx: commands.Context):
        if not await self.client.validator.server_registered(ctx):
            return

        guild = self.client.validator.require_guild(ctx)
        clan = await self.client.service.get_clan(guild.id)
        war = await self.client.service.get_current_war(guild.id)

        if not war:
            await ctx.send(
                "⛔ No current war found for your clan. Is your clan war history public? 🤔"
            )
            return

        if not war.clan or not war.opponent:
            await ctx.send("⛔ Incomplete war data.")
            return

        embed = discord.Embed(
            title=f"{clan.name} War Status",
            description=(
                f"State: {war.state}\n"
                f"Team Size: {war.team_size}\n"
                f"Clan Score: {war.clan.score}\n"
                f"Opponent Score: {war.opponent.score}\n"
                f"Stars: {war.clan.stars}\n"
                f"Destruction: {war.clan.destruction_percentage}%\n"
                f"Opponent Stars: {war.opponent.stars}\n"
                f"Opponent Destruction: {war.opponent.destruction_percentage}%\n"
            ),
            color=0x00FF00,
        )

        await ctx.send(embed=embed)


async def setup(client: Bot):
    await client.add_cog(War(client))
