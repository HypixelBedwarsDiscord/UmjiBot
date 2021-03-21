import time

from discord.ext import commands
import discord

ROLES = {
    "STAFF": 724465434358841384,
    "NEED_USERNAME": 480448464220585984
}
GUILD_ID = 384804710110199809
# VERIFICATION_CHANNEL_ID = 422259585798242314
VERIFICATION_CHANNEL_ID = 0
TIME_BETWEEN_AUTO = 86400  # 24 hours in seconds
DISCORD_NOT_LINKED_ERROR = """
You have not linked your discord tag on Hypixel!
1. Go to any lobby.
2. Right click your player head.
3. Click the social media menu (Twitter icon).
4. Click the Discord icon.
5. Paste your Discord tag when asked (e.g. Lite#0001).
6. Head back to <#422259585798242314> and run "r.verify <username>" with username being your Minecraft username.

--> Example: r.verify Poggos

If you need more help, view <#614994890790666242>"""


async def guild_check(ctx):
    return ctx.guild and ctx.guild.id == GUILD_ID


async def verify_check(ctx):
    return ctx.channel.id == VERIFICATION_CHANNEL_ID


class Bedwars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self._initialize())
        self.auto = {}

    async def _initialize(self):
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(GUILD_ID)
        self.staff_role = self.guild.get_role(ROLES.get("STAFF"))
        self.need_username_role = self.guild.get_role(ROLES.get("NEED_USERNAME"))

    @commands.command(aliases=["v", "bwverify"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.check(verify_check)
    async def verify(self, ctx: commands.Context, query: str):
        if user := await self.bot.data.get(ctx.author.id):
            if bool(user.uuid):
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are already verified!"))
            elif user.blacklisted:
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are blacklisted from verification!"))
        player = await self.bot.hypixel.player.get(query=query)
        # guild = await self.bot.hypixel.guild.get(name=player.name)
        if str(ctx.author) != player.social.discord:
            return await ctx.reply(embed=self.bot.static.embed(ctx, DISCORD_NOT_LINKED_ERROR))
        await self.bot.data.set(ctx.author.id, "uuid", player.uuid)
        await self._verify(ctx.author, player)
        await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified you as {ctx.author.mention}"))
        return await ctx.message.delete()

    @commands.command(aliases=["bwupdate", "u"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    async def update(self, ctx: commands.Context):
        user = await self.bot.data.get(ctx.author.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, "You are not verified! Verify first with "
                                                                    "`r.verify <your-ign>`"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(ctx.author, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, "Updated your roles and nickname!"))

    @commands.command(aliases=["fu"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def forceupdate(self, ctx: commands.Context, target: discord.Member):
        user = await self.bot.data.get(target.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, f"{target.mention} is not verified!"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(target, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Updated {target.mention}'s roles and nickname!"))

    @commands.command(aliases=["fv"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def forceverify(self, ctx: commands.Context, target: discord.Member, query: str):
        player = await self.bot.hypixel.player.get(query=query)
        # guild = await self.bot.hypixel.guild.get(name=player.name)
        await self.bot.data.set(target.id, "uuid", player.uuid)
        await self._verify(target, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified {target.mention} as {player}"))

    @commands.command(aliases=["forceunverify", "uv", "fuv"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def unverify(self, ctx: commands.Context, target: discord.Member):
        # guild = await self.bot.hypixel.guild.get(name=player.name)
        data = await self.bot.data.get(target.id)
        if not data: return await ctx.reply(embed=self.bot.static.embed(ctx, f"{target.mention} was not verified!"))
        await self.bot.data.set(target.id, "uuid", None)
        await self._unverify(target)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Unverified {target.mention}"))

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def blacklist(self, ctx: commands.Context, target: discord.Member):
        data = await self.bot.data.get(target.id)
        action = not data.blacklisted
        await self.bot.data.set(target.id, "blacklisted", action)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Blacklisted {target.mention}" if action else f"Unblacklisted {target.mention}"))

    async def _verify(self, target: discord.Member, player):
        index = player.bedwars.prestige.star_index
        index = 30 if player.bedwars.prestige.star_index > 30 else index
        role = self.bot.prestiges.all[index]
        if not role.role: role.get(self.guild)
        await target.edit(nick=f"[{player.bedwars.prestige.star} {role.star}] {player.name}")
        if role.role not in target.roles:
            for old in self.bot.prestiges.all:
                if not old.role: old.get(self.guild)
                if old.role in target.roles: await target.remove_roles(old)
        await target.add_roles(role)
        await target.remove_roles(self.need_username_role)

    async def _unverify(self, target: discord.Member):
        for role in self.bot.prestiges.all:
            if not role.role: role.get(self.guild)
            if role.role in target.roles: await target.remove_roles(role.role)
        await target.add_roles(self.need_username_role)
        await target.edit(nick=None)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if not self.bot.is_ready or not message.guild or not message.guild.id == GUILD_ID: return
    #     if last := self.auto.get(message.author.id):
    #         if time.time() - last < TIME_BETWEEN_AUTO:
    #             return
    #     user = await self.bot.data.get(message.author.id)
    #     if not user or not bool(user.uuid): return
    #     player = await self.bot.hypixel.player.get(uuid=user.uuid)
    #     print(message.author)
    #     try:
    #         await self._verify(message.author, player)
    #     except discord.Forbidden:
    #         pass
    #     self.auto[message.author.id] = time.time()


def setup(bot):
    bot.add_cog(Bedwars(bot))
    print("Reloaded cogs.bedwars")
