from discord.ext import commands, menus
import discord


class Static:
    def __init__(self):
        self.paginators = Paginators()
        self.roles = Roles()
        self.channels = Channels()
        self.guild = 384804710110199809

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
        self.dict = {
            "STAFF": 724465434358841384,
            "NEED_USERNAME": 470511160412733441,
            "NEED_USERNAMES": 480448464220585984,
            "GUILDS": {
                "5c8609a877ce849ebc770053": 822593831321075762,  # thorn v2
                "5af718d40cf2cbe7a9eeb063": 823291974471385139  # Calm
            },
            "HYPIXEL": {
                "STAFF": 416614910299209738,
                "ADMIN": 423307128091181059,
                "MOD": 423307060457897985,
                "YOUTUBE": 430157044041908234
            }
        }
        self.staff = 724465434358841384
        self.need_username = 470511160412733441
        self.need_usernames = 480448464220585984

    def get(self, guild):
        self.staff = guild.get_role(self.staff)
        self.need_username = guild.get_role(self.need_username)
        self.need_usernames = guild.get_role(self.need_usernames)


class Channels:
    def __init__(self):
        self.verification = 422259585798242314
        self.logs = 672475663994716178

    def get(self, guild):
        self.verification = guild.get_channel(self.verification)
        self.logs = guild.get_channel(self.logs)


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
