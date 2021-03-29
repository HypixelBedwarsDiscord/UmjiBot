import os
import traceback

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
        extensions = [os.path.join(dp, f) for dp, dn, fn in os.walk("cogs") for f in fn] + \
                     [os.path.join(dp, f) for dp, dn, fn in os.walk("commands") for f in fn] + \
                     [os.path.join(dp, f) for dp, dn, fn in os.walk("events") for f in fn] + \
                     [os.path.join(dp, f) for dp, dn, fn in os.walk("modules") for f in fn]
        for file in extensions[:]:
            if not file.endswith(".py"):  # these are special cases
                extensions.remove(file)
        for extension in extensions:
            try:
                self.bot.load_extension(((extension.replace("/", "."))[:-3]) if extension.endswith(".py") else extension)
            except Exception as error:
                exception = f"{type(error).__name__}: {error}"
                print("Failed to load extension {}\n{}".format(extension, exception))
                print(f"Failed to load extensions {extension}\n{exception}")
                print("".join(traceback.format_exception(type(error), error, error.__traceback__)))
        ready_time = datetime.utcnow()
        ready_time_est = pytz.utc.localize(ready_time).astimezone(pytz.timezone("America/New_York"))
        print(f"Connected to Discord at {ready_time_est.strftime('%A, %b %d, %Y - %m/%d/%Y - %I:%M:%S %p')}")


def setup(bot):
    print("Initializing")
    bot.add_cog(Initialize(bot))
