from discord.ext import commands, menus
import discord

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        

    
def setup(bot):
    bot.add_cog(Moderation(bot))
    print("Reloaded cogs.moderation")