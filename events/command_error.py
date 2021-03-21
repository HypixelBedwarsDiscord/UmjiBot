import traceback

from discord.ext import commands
import discord


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        ignored = (commands.CommandNotFound,
                   commands.CheckFailure
                   )
        if isinstance(error, ignored): return
        await ctx.reply(embed=self.bot.static.embed(ctx, f"```{''.join(traceback.format_exception(type(error), error, error.__traceback__))}```"))


def setup(bot):
    bot.add_cog(CommandError(bot))
    print("Reloaded events.command_error")
