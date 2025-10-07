import coc
import discord

from discord.ext import commands

from core.bot import Bot


class War(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command(name="war")
    async def war(self, ctx: commands.Context):
        if not await self.client.validator.user_registered(ctx):
            return

        clan = await self.client.service.get_clan(ctx.author.id)
        war = await self.client.service.get_current_war(ctx.author.id)

        if not war:
            await ctx.send("⛔ No current war found for your clan.")
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
