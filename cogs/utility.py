"""
MIT License

Copyright (c) 2020 Myer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands, menus

GUILD_ID = 384804710110199809


async def guild_check(ctx):
    return ctx.guild and ctx.guild.id == GUILD_ID


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["lrm"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(724465434358841384)  # staff
    async def listrolemembers(self, ctx: commands.Context, role: discord.Role):
        result = [member.mention for member in role.members]
        await menus.MenuPages(source=self.bot.static.paginators.regular(result, ctx, discord.Embed(
            title=f"{len(result)} with {role}",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        ))).start(ctx)

    @commands.command(aliases=["lcm"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(724465434358841384)  # staff
    async def listchannelmembers(self, ctx: commands.Context, channel: discord.TextChannel = None):
        if not channel: channel = ctx.channel
        result = [member.mention for member in channel.members]
        await menus.MenuPages(source=self.bot.static.paginators.regular(result, ctx, discord.Embed(
            title=f"{len(result)} in {channel}",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        ))).start(ctx)


def setup(bot):
    bot.add_cog(Utility(bot))
    print("Reloaded cogs.utility")
