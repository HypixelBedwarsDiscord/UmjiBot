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
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def help(self, ctx):
        if self.bot.static.roles.staff in ctx.author.roles:
            message = "`r.update (r.u)`: Updates your star, nickname, and roles\n" \
                      "`r.verify`: Verifies you with your Minecraft Account Name\n" \
                      "**__Staff Commands__**:\n" \
                      "`r.fv <user-id> <ign>` Force verifies someone\n" \
                      "`r.fu <user-id>` Force updates someone\n" \
                      "`r.fvm <message-id>` Force verifies someone based off a verify attempt of a message **FROM THEM**\n" \
                      "`r.fuv <user-id>` Force unverifies someone\n" \
                      "`r.blacklist` <user-id> Blacklists someone from using `r.verify`"
        else:
            message = "`r.update (r.u)`: Updates your star, nickname, and roles\n" \
                      "`r.verify`: Verifies you with your Minecraft Account Name\n"
        await ctx.reply(embed=discord.Embed(
            name="Help",
            description=message,
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ).set_author(
            name="Help",
            icon_url=str(ctx.me.avatar_url_as(static_format="png", size=2048))
        ))


def setup(bot):
    bot.remove_command("help")
    print("Unloaded default help command")
    bot.add_cog(Help(bot))
    print("Reloaded commands.help")
