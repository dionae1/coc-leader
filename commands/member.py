import coc
import discord

from discord.ext import commands
from typing import List

from core.bot import Bot


class Member(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command(name="members")
    async def members(self, ctx: commands.Context):
        if not await self.client.validator.server_registered(ctx):
            return

        guild = self.client.validator.require_guild(ctx)
        clan = await self.client.service.get_clan(guild.id)

        members: List[coc.ClanMember] = sorted(
            clan.members,
            key=lambda m: m.trophies,
            reverse=True,
        )

        embed = discord.Embed(
            title=f"{clan.name}\n- {len(members)} Members",
            color=0x00FF00,
        )

        lines = []
        for m in members:
            lines.append(f"{m.trophies:^10} {m.name:^15} {m.role:^15}")

        embed.description = (
            f"```\n{'🏆 Trophy':^10} {'👤 Player':^15} {'💼 Role':^12}\n"
            f"\n" + "\n".join(lines) + "\n```"
        )

        await ctx.send(embed=embed)

    @commands.command(name="member")
    async def member(self, ctx: commands.Context, player_tag: str):
        if not await self.client.validator.server_registered(ctx):
            return

        try:
            member = await self.client.service.get_member(player_tag)

            embed = discord.Embed(title="Member Information", color=0x00FF00)
            embed.add_field(name="Name", value=member.name, inline=True)
            embed.add_field(name="Tag", value=member.tag, inline=True)
            embed.add_field(name="Town Hall Level", value=member.town_hall, inline=True)
            embed.add_field(name="Role", value=member.role, inline=True)
            embed.add_field(name="Exp Level", value=member.exp_level, inline=True)
            embed.add_field(name="War Stars", value=member.war_stars, inline=True)
            embed.add_field(name="Up to wars?", value=member.war_opted_in, inline=True)

            await ctx.send(embed=embed)

        except ValueError as e:
            await ctx.send(str(e))


async def setup(client: Bot):
    await client.add_cog(Member(client))
