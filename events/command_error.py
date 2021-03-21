import traceback
import sys

from discord.ext import commands
import discord

import hypixelaPY


INVALID_MINECRAFT_ACCOUNT_ERROR = """
{user}, player not found.

The username you entered could not be found on Hypixel.
   - Make sure you typed your username correctly (the casing does not matter).
   - Try joining Hypixel before running this command again. If you can't connect (e.g., "failed to authenticate"), try signing out of Minecraft from the launcher, signing back in, and rejoin Hypixel.
   - Make sure you typed your Minecraft username and not your Discord username/tag."""


class CommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not self.bot.is_ready: return
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
                embed=ctx.bot.static.embed(ctx, f"""{ctx.author.mention}, player not found.
The username you entered could not be found on Hypixel.
   - Make sure you typed your username correctly (the casing does not matter).
   - Try joining Hypixel before running this command again. If you can't connect (e.g., "failed to authenticate"), try signing out of Minecraft from the launcher, signing back in, and rejoin Hypixel.
   - Make sure you typed your Minecraft username and not your Discord username/tag."""))
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.name == "verify":
                return await ctx.reply(
                    embed=self.bot.static.embed(ctx, f"You must provide a Minecraft Username to verify with. For "
                                                     f"example, `r.verify myerfire`"))
            return await ctx.reply(
                embed=self.bot.static.embed(ctx, f"{error.param} is a required argument that is missing"))
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
