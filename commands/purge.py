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

from discord.ext import commands


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.has_role(724465434358841384)  # staff
    async def purge(self, ctx, limit: int):
        start = await ctx.reply(embed=self.bot.static.embed(ctx, f"Starting purge for {limit} messages. This could "
                                                                 f"take a LONG time if the messages being deleted are "
                                                                 f"over 14 days old."))
        await ctx.channel.purge(limit=limit + 2, check=lambda m: m.id != start.id)
        # +2 because one is the command message, one is the start message
        await start.delete()
        return await ctx.send(f"Purged {limit} messages", delete_after=5)


def setup(bot):
    bot.add_cog(Purge(bot))
    print("Reloaded commands.purge")
