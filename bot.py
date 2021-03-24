import asyncio
import os

from discord.ext import commands
import discord
import hypixelaPY

from config import Config
from data import DataConnect
from prestiges import Prestiges
from static import Static

config_ = Config()
bot = commands.Bot(
    command_prefix="r.",
    owner_id=config_.owner,
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False)
)
bot.config = config_
bot.prestiges = Prestiges()
bot.static = Static()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"


@bot.check
async def ready(ctx):
    return ctx.bot.is_ready()


async def start():
    bot.hypixel = await hypixelaPY.Hypixel(bot.config.keys.hypixel)
    bot.data = await DataConnect(bot.config.keys.postgres)
    bot.load_extension("initialize")
    bot.load_extension("jishaku")
    await bot.start(bot.config.keys.token)


async def stop():
    await bot.data.data.release()
    await bot.logout()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start())
    except KeyboardInterrupt:
        asyncio.get_event_loop().run_until_complete(stop())
