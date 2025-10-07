import discord

from discord.ext import commands

from core.bot import Bot


class Clan(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command(name="clan")
    async def clan(self, ctx: commands.Context):
        if not await self.client.validator.user_registered(ctx):
            return

        clan = await self.client.service.get_clan(ctx.author.id)

        clan_name = clan.name
        clan_tag = clan.tag
        members_count = clan.member_count

        embed = discord.Embed(title=clan_name, color=0x00FF00)

        badge = clan.badge
        if badge and hasattr(badge, "small"):
            embed.set_thumbnail(url=badge.small)

        members = clan.members
        leader = next((m for m in members if m.role == "leader"), None)

        embed.description = f"\n< *{clan_tag}* >"

        if leader:
            embed.add_field(name=f"Leader:", value=leader.name, inline=False)

        embed.add_field(name="Level", value=clan.level, inline=True)
        embed.add_field(name="Points", value=clan.points, inline=True)
        embed.add_field(name="League", value=clan.war_league, inline=True)
        embed.add_field(name="Members", value=members_count, inline=True)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Clan(client))
