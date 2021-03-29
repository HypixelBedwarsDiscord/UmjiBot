from discord.ext import commands
import discord


class Boosts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.bot.is_ready(): return
        if not message.channel == self.bot.static.channels.boosts: return
        if not message.type == discord.MessageType.premium_guild_subscription: return
        return await message.add_reaction(":yellow_heart:")


def setup(bot):
    bot.add_cog(Boosts(bot))
    print("Reloaded modules.boosts")
