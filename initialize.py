from discord.ext import commands
from datetime import datetime
import pytz


class Initialize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())

    async def initialize(self):
        print("Waiting for internal cache")
        await self.bot.wait_until_ready()
        print("Internal cache is ready")
        self.bot.config.channels.get(self.bot)
        self.bot.static.get(self.bot)
        self.bot.static.roles.get(self.bot.static.guild)
        self.bot.static.channels.get(self.bot.static.guild)
        ready_time = datetime.utcnow()
        ready_time_est = pytz.utc.localize(ready_time).astimezone(pytz.timezone("America/New_York"))
        print(f"Connected to Discord at {ready_time_est.strftime('%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p')}")


def setup(bot):
    print("Initializing")
    bot.add_cog(Initialize(bot))
