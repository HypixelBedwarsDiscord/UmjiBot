from discord.ext import commands
import discord

class TicketCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if not self.bot.is_ready(): return
        if not channel.category.id == self.bot.static.channels.categories.tickets.id: return
        if not channel.name.startswith("ticket-"): return
        return await channel.send(self.bot.static.roles.support.mention)
       

def setup(bot):
    bot.add_cog(TicketCreate(bot))
    print("Reloaded events.ticket_create")
