from discord.ext import commands
import discord

GUILD_ID = 384804710110199809
VERIFICATION_CHANNEL_ID = 0
STAFF_ROLE_ID = 724465434358841384
NEED_USERNAME_ROLE_ID = 480448464220585984


async def check(ctx):
    return ctx.guild.id == GUILD_ID
    #  and ctx.channel.id == VERIFICATION_CHANNEL_ID


class Bedwars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self._initialize())

    async def _initialize(self):
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(GUILD_ID)
        self.staff_role = self.guild.get_role(STAFF_ROLE_ID)
        self.need_username_role = self.guild.get_role(NEED_USERNAME_ROLE_ID)

    @commands.command(aliases=["v"])
    @commands.check(check)
    async def verify(self, ctx: commands.Context, query: str):
        if user := await self.bot.data.get(ctx.author.id):
            if bool(user.uuid):
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are already verified!"))
            elif user.blacklisted:
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are blacklisted from verification!"))
        player = await self.bot.hypixel.player.get(query=query)
        # guild = await self.bot.hypixel.guild.get(name=player.name)
        if str(ctx.author) != player.social.discord:
            return await ctx.reply(embed=self.bot.static.embed(ctx, "Set your Discord name and tag on Hypixel first!"))
        await self.bot.data.set(ctx.author.id, "uuid", player.uuid)
        await self._verify(ctx.author, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified you as {ctx.author.mention}"))

    @commands.command(aliases=["bwupdate", "u"])
    @commands.check(check)
    async def update(self, ctx: commands.Context):
        user = await self.bot.data.get(ctx.author.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, "You are not verified! Verify first with "
                                                                    "`r.verify <your-ign>`"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(ctx.author, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, "Updated your roles and nickname!"))

    @commands.command()
    @commands.check(check)
    @commands.has_role(STAFF_ROLE_ID)
    async def forceupdate(self, ctx: commands.Context, target: discord.Member):
        user = await self.bot.data.get(target.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, f"{target.mention} is not verified!"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(target, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Updated {target.mention}'s roles and nickname!"))

    @commands.command(aliases=["fv"])
    @commands.check(check)
    @commands.has_role(STAFF_ROLE_ID)
    async def forceverify(self, ctx: commands.Context, target: discord.Member, query: str):
        player = await self.bot.hypixel.player.get(query=query)
        # guild = await self.bot.hypixel.guild.get(name=player.name)
        await self.bot.data.set(target.id, "uuid", player.uuid)
        await self._verify(target, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified {target.mention} as {player}"))

    @commands.command(aliases=["forceunverify", "uv", "fuv"])
    @commands.check(check)
    @commands.has_role(STAFF_ROLE_ID)
    async def unverify(self, ctx: commands.Context, target: discord.Member):
        # guild = await self.bot.hypixel.guild.get(name=player.name)
        data = await self.bot.data.get(target.id)
        if not data: return await ctx.reply(embed=self.bot.static.embed(ctx, f"{target.mention} was not verified!"))
        await self.bot.data.set(target.id, "uuid", None)
        await self._unverify(target)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Unverified {target.mention}"))

    @commands.command()
    @commands.check(check)
    @commands.has_role(STAFF_ROLE_ID)
    async def blacklist(self, ctx: commands.Context, target: discord.Member):
        data = await self.bot.data.get(target.id)
        action = not data.blacklisted
        await self.bot.data.set(target.id, "blacklist", action)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Blacklisted {target.mention}" if action else f"Unblacklisted {target.mention}"))

    async def _verify(self, target: discord.Member, player):
        index = player.bedwars.prestige.star_index
        index = 30 if player.bedwars.prestige.star_index > 30 else index
        role = self.bot.prestiges.all[index]
        if not role.role: role.get(self.guild)
        await target.edit(nick=f"[{player.bedwars.prestige.star}{role.star}] {player.name}")
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


def setup(bot):
    bot.add_cog(Bedwars(bot))
    print("Reloaded cogs.bedwars")
