from discord.ext import commands
import discord


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, error):
        error = getattr(error, "original", error)
        ignored = (commands.CommandNotFound,
                   commands.CheckFailure
                   )
        pass


def setup(bot):
    bot.add_cog(CommandError(bot))
    print("Reloaded events.command_error")
