from discord.ext import menus
import discord

STAFF_ROLE_ID = 724465434358841384
GUILD_ID = 384804710110199809
VERIFICATION_CHANNEL_ID = 422259585798242314
COMMANDS_CHANNEL_ID = 398619687291715604


async def guild_check(ctx):
    return ctx.guild and ctx.guild.id == GUILD_ID


async def commands_channel_check(ctx):
    return ctx.channel.id == COMMANDS_CHANNEL_ID


async def verification_channel_check(ctx):
    return ctx.channel.id == VERIFICATION_CHANNEL_ID


async def update_check(ctx):
    return ctx.channel.id == COMMANDS_CHANNEL_ID or ctx.channel.id == VERIFICATION_CHANNEL_ID


async def verification_check(ctx):
    # this is likely temporary, there were a thousand or so people who need to reverify
    # despite already being out of the verification channel
    if ctx.channel.id == VERIFICATION_CHANNEL_ID: return True  # always should work in #verification
    if ctx.channel.id != COMMANDS_CHANNEL_ID: return False
    user = await ctx.bot.data.get(ctx.author.id)
    if not user or not bool(user.uuid):
        return True
    return bool(user) or bool(user)


class Static:
    def __init__(self):
        self.paginators = Paginators()
        self.roles = Roles()
        self.channels = Channels()
        self.guild = GUILD_ID

    def get(self, bot):
        self.guild = bot.get_guild(self.guild)

    @staticmethod
    def embed(ctx, description):
        return discord.Embed(
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
            description=description
        )

    @staticmethod
    def plancke_url(uuid):
        return f"https://plancke.io/hypixel/player/stats/{uuid}"


class Roles:
    def __init__(self):
        self.staff = 724465434358841384
        self.support = 459841215945375757
        self.need_usernames = 480448464220585984
        self.verified = 840265827831382076
        self.hypixel = HypixelRoles()

    def get(self, guild):
        self.staff = guild.get_role(self.staff)
        self.support = guild.get_role(self.support)
        self.need_usernames = guild.get_role(self.need_usernames)
        self.verified = guild.get_role(self.verified)
        self.hypixel.get(guild)


class HypixelRoles:
    def __init__(self):
        self.staff = 416614910299209738
        self.admin = 423307128091181059
        self.mod = 423307060457897985
        self.youtube = 430157044041908234
        self.dict = None

    def get(self, guild):
        self.staff = guild.get_role(self.staff)
        self.admin = guild.get_role(self.admin)
        self.mod = guild.get_role(self.mod)
        self.youtube = guild.get_role(self.youtube)
        self.dict = {
            "STAFF": self.staff,
            "ADMIN": self.admin,
            "MOD": self.mod,
            "YOUTUBE": self.youtube
        }


class Channels:
    def __init__(self):
        self.verification = VERIFICATION_CHANNEL_ID
        self.logs = 672475663994716178
        self.commands = COMMANDS_CHANNEL_ID
        self.boosts = 691369961108799569
        self.verification_list_30 = 855649436591325194
        self.categories = Categories()

    def get(self, guild):
        self.verification = guild.get_channel(self.verification)
        self.logs = guild.get_channel(self.logs)
        self.commands = guild.get_channel(self.commands)
        self.boosts = guild.get_channel(self.boosts)
        self.verification_list_30 = guild.get_channel(self.verification_list_30)
        self.categories.get(guild)


class Categories:
    def __init__(self):
        self.tickets = 459835600913039360

    def get(self, guild):
        self.tickets = guild.get_channel(self.tickets)


class Paginators:
    def __init__(self):
        self.regular = Paginator
        self.codeblock = CodeblockPaginator


class Paginator(menus.ListPageSource):
    def __init__(self, data, ctx, embed):
        self.ctx = ctx
        self.embed = embed
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        self.embed.description = f"{joined}"
        return self.embed


class CodeblockPaginator(menus.ListPageSource):
    def __init__(self, data, ctx, embed):
        self.ctx = ctx
        self.embed = embed
        super().__init__(data, per_page=15)

    async def format_page(self, menu, entries):
        joined = "\n".join(entries)
        self.embed.description = f"```{joined}```"
        return self.embed
