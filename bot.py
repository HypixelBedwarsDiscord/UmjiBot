import asyncio
import os

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

extensions = [
    "jishaku",
    "verify"
]
for extension in extensions:
    bot.load_extension(extension)


async def main():
    bot.hypixel = await hypixelaPY.Hypixel(bot.config.keys.hypixel)
    await bot.start(bot.config.keys.token)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
