import asyncio
import os
import traceback

from discord.ext import commands
import discord
import hypixelaPY

from config import Config
from data import Data
from prestiges import Prestiges
from static import Static

bot = commands.Bot(
    command_prefix="r.",
    owner_id=0,
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False)
)
bot.config = Config()
bot.data = Data()
bot.prestiges = Prestiges()
bot.static = Static()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

extensions = [os.path.join(dp, f) for dp, dn, fn in os.walk("cogs") for f in fn] + \
             [os.path.join(dp, f) for dp, dn, fn in os.walk("events") for f in fn] + \
             ["jishaku"]
for file in extensions[:]:
    if not file.endswith(".py") and file not in ["jishaku"]:  # jishaku is a special case
        extensions.remove(file)

for extension in extensions:
    try:
        bot.load_extension(((extension.replace("/", "."))[:-3]) if extension.endswith(".py") else extension)
    except Exception as error:
        exception = f"{type(error).__name__}: {error}"
        print("Failed to load extension {}\n{}".format(extension, exception))
        print(f"Failed to load extensions {extension}\n{exception}")
        print("".join(traceback.format_exception(type(error), error, error.__traceback__)))


async def start():
    bot.hypixel = await hypixelaPY.Hypixel(bot.config.keys.hypixel)
    await bot.start(bot.config.keys.token)


async def stop():
    await bot.logout()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start())
    except KeyboardInterrupt:
        asyncio.get_event_loop().run_until_complete(stop())
