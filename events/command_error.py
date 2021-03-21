import traceback
import sys

from discord.ext import commands
import discord

import hypixelaPY


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        ignored = (commands.CommandNotFound,
                   commands.CheckFailure
                   )
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.MaxConcurrencyReached):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"{ctx.author.mention}, you are sending commands too fast"))
        elif isinstance(error, hypixelaPY.NoPlayerFoundError):
            return await ctx.reply(
                embed=ctx.bot.static.embed(ctx, f"{ctx.author.mention}, \"{error}\" is not a valid Minecraft account"))
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.reply(
                embed=self.bot.static.embed(ctx, f"{ctx.author.mention}, `{error.param}` is a required "
                                                 f"argument that is missing"))
        await ctx.reply(embed=self.bot.static.embed(ctx, str(error)))
        error_traceback = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        await ctx.bot.config.channels.errors.send(embed=discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            title=f"Ignoring exception in command {ctx.command}\n"
                  f"`{ctx.message.content}`",
            description=(f"in guild `{ctx.guild.name} ({ctx.guild.id})`\n"
                         if isinstance(ctx.message.channel, discord.TextChannel) else
                         "in a DM channel\n") + f"invoked by {ctx.author.mention} ({ctx.author}) [{ctx.author.id}]\n"
                                                f"```{error_traceback}```"))
        print(f"Ignoring exception in command {ctx.command}", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandError(bot))
    print("Reloaded events.command_error")
