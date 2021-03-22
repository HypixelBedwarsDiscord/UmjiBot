import time

from discord.ext import commands, menus
import discord

import hypixelaPY

ROLES = {
    "STAFF": 724465434358841384,
    "NEED_USERNAME": 480448464220585984,
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
GUILD_ID = 384804710110199809
VERIFICATION_CHANNEL_ID = 422259585798242314
COMMANDS_CHANNEL_ID = 398619687291715604
# VERIFICATION_CHANNEL_ID = 0
TIME_BETWEEN_AUTO = 86400  # 24 hours in seconds


async def guild_check(ctx):
    return ctx.guild and ctx.guild.id == GUILD_ID


async def verification_channel_check(ctx):
    return ctx.channel.id == VERIFICATION_CHANNEL_ID


async def verification_check(ctx):  # this is likely temporary, there were a thousand or so people who need to reverify
    # despite already being out of the verification channel
    if ctx.channel.id == VERIFICATION_CHANNEL_ID: return True
    if not ctx.channel.id == COMMANDS_CHANNEL_ID: return False
    user = await ctx.bot.data.get(ctx.author.id)
    if not user or not bool(user.uuid):
        return True
    return ctx.channel.id == COMMANDS_CHANNEL_ID


async def commands_channel_check(ctx):
    return ctx.channel.id == COMMANDS_CHANNEL_ID


class Bedwars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self._initialize())
        self.auto = {}

    async def cog_check(self, ctx):
        return self.bot.is_ready

    async def _initialize(self):
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(384804710110199809)
        self.logs = self.guild.get_channel(672475663994716178)
        self.verification = self.bot.get_channel(422259585798242314)
        self.staff_role = self.guild.get_role(ROLES.get("STAFF"))
        self.need_username_role = self.guild.get_role(ROLES.get("NEED_USERNAME"))
        self.guild_roles = {
            "5c8609a877ce849ebc770053": self.guild.get_role(ROLES["GUILDS"].get("5c8609a877ce849ebc770053")),
            "5af718d40cf2cbe7a9eeb063": self.guild.get_role(ROLES["GUILDS"].get("5af718d40cf2cbe7a9eeb063"))
        }
        self.hypixel_roles = {
            "STAFF": {
                "STAFF": self.guild.get_role(ROLES["HYPIXEL"].get("STAFF")),
                "MOD": self.guild.get_role(ROLES["HYPIXEL"].get("MOD")),
                "ADMIN": self.guild.get_role(ROLES["HYPIXEL"].get("ADMIN"))
            },
            "YOUTUBE": self.guild.get_role(ROLES["HYPIXEL"].get("YOUTUBE"))
        }

    @commands.command(aliases=["v", "bwverify"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.check(verification_check)
    async def verify(self, ctx: commands.Context, query: str):
        if user := await self.bot.data.get(ctx.author.id):
            if bool(user.uuid):
                await self.logs.send(embed=discord.Embed(
                    title="Verification Failed",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at,
                    description="User was already verified"
                ).add_field(
                    name="Member",
                    value=f"{ctx.author.mention} ({ctx.author}) [{ctx.author.id}]"
                ).add_field(
                    name="Moderator",
                    value=ctx.me.mention
                ))
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are already verified!"))
            elif user.blacklisted:
                await self.logs.send(embed=discord.Embed(
                    title="Verification Failed",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at,
                    description="User is blacklisted from verification"
                ).add_field(
                    name="Member",
                    value=f"{ctx.author.mention} ({ctx.author}) [{ctx.author.id}]"
                ).add_field(
                    name="Moderator",
                    value=ctx.me.mention
                ))
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are blacklisted from verification!"))
        player = await self.bot.hypixel.player.get(query=query)
        if not bool(player.social.discord):
            await self.logs.send(embed=discord.Embed(
                title="Verification Failed",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at,
                description="Minecraft account did not have a Discord name set on Hypixel"
            ).add_field(
                name="Member",
                value=f"{ctx.author.mention} ({ctx.author}) [{ctx.author.id}]"
            ).add_field(
                name="Moderator",
                value=ctx.me.mention
            ).add_field(
                name="Minecraft Account",
                value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
            ))
            return await ctx.reply(embed=self.bot.static.embed(ctx, f"You have not linked your Discord tag on Hypixel!\n"
                                                                    f"1. Go to any lobby.\n"
                                                                    f"2. Right click your player head.\n"
                                                                    f"3. Click the social media menu. (Twitter icon)\n"
                                                                    f"4. Click the Discord icon.\n"
                                                                    f"5. Paste your Discord tag when asked (e.g. "
                                                                    f"Lite#0001).\n "
                                                                    f"6. Head back to <#422259585798242314> and run "
                                                                    f"`r.verify <username>` with username being your "
                                                                    f"Minecraft username.\n\n"
                                                                    f"--> Example: `r.verify Poggos`\n\n"
                                                                    f"If you need more help, view <#614994890790666242>"))
        elif str(
                ctx.author) != player.social.discord and f"{str(ctx.author.id)[-6:]}#{ctx.author.discriminator}" != player.social.discord:
            await self.logs.send(embed=discord.Embed(
                title="Verification Failed",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at,
                description="Minecraft account's Discord on Hypixel does not match verification requester"
            ).add_field(
                name="Member",
                value=f"{ctx.author.mention} ({ctx.author}) [{ctx.author.id}]"
            ).add_field(
                name="Moderator",
                value=ctx.me.mention
            ))
            return await ctx.reply(embed=self.bot.static.embed(ctx, f"{ctx.author.mention}, this player's Discord tag "
                                                                    f"does not match with your current tag. The "
                                                                    f"Discord tag {player.social.discord} on Hypixel "
                                                                    f"does not match your current tag "
                                                                    f"`({str(ctx.author)})`, or short ID form "
                                                                    f"`({str(ctx.author.id)[-6:]}#{ctx.author.discriminator})`."
                                                                    f"You must verify with your own Minecraft "
                                                                    f"Account's name"))
        await self.bot.data.set(ctx.author.id, "uuid", player.uuid)
        await self._verify(ctx.author, player)
        await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified you as {ctx.author.mention}"), delete_after=5)
        await self.logs.send(embed=discord.Embed(
            title="Member Verified",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        ).add_field(
            name="Member",
            value=f"{ctx.author.mention} ({ctx.author}) [{ctx.author.id}]"
        ).add_field(
            name="Moderator",
            value=ctx.me.mention
        ).add_field(
            name="Minecraft Account",
            value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
        ))
        await ctx.message.delete()
        return await self.verification.purge(check=lambda m: m.author.id == ctx.author.id)

    @commands.command(aliases=["bwupdate", "u"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.check(commands_channel_check)
    async def update(self, ctx: commands.Context):
        user = await self.bot.data.get(ctx.author.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, "You are not verified! Verify first with "
                                                                    "`r.verify <your-ign>`"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(ctx.author, player)
        await self.logs.send(embed=discord.Embed(
            title="Member Updated (On User Command)",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at,
        ).add_field(
            name="Member",
            value=f"{ctx.author.mention} ({ctx.author}) [{ctx.author.id}]"
        ).add_field(
            name="Moderator",
            value=ctx.me.mention
        ).add_field(
            name="Minecraft Account",
            value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
        ))
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
        await self.logs.send(embed=discord.Embed(
            title="Member Force Updated",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at,
        ).add_field(
            name="Member",
            value=f"{target.mention} ({target}) [{target.id}]"
        ).add_field(
            name="Moderator",
            value=ctx.author.mention
        ).add_field(
            name="Minecraft Account",
            value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
        ))
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Updated {target.mention}'s roles and nickname!"))

    @commands.command(aliases=["fv"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def forceverify(self, ctx: commands.Context, target: discord.Member, query: str):
        player = await self.bot.hypixel.player.get(query=query)
        await self.bot.data.set(target.id, "uuid", player.uuid)
        await self._verify(target, player)
        await self.logs.send(embed=discord.Embed(
            title="Member Force Verified",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        ).add_field(
            name="Member",
            value=f"{target.mention} ({target}) [{target.id}]"
        ).add_field(
            name="Moderator",
            value=ctx.author.mention
        ).add_field(
            name="Minecraft Account",
            value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
        ))
        await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified {target.mention} as {player}"), delete_after=5)
        await ctx.message.delete()
        return await self.verification.purge(check=lambda m: m.author.id == target.id)

    @commands.command(aliases=["forceunverify", "uv", "fuv"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def unverify(self, ctx: commands.Context, target: discord.Member):
        data = await self.bot.data.get(target.id)
        if not data or not bool(data.uuid): return await ctx.reply(
            embed=self.bot.static.embed(ctx, f"{target.mention} was not verified!"))
        await self.bot.data.set(target.id, "uuid", None)
        await self._unverify(target)
        await self.logs.send(embed=discord.Embed(
            title="Member Unverified",
            color=discord.Color.red(),
            timestamp=ctx.message.created_at,
        ).add_field(
            name="Member",
            value=f"{target.mention} ({target}) [{target}]"
        ).add_field(
            name="Moderator",
            value=ctx.author.mention
        ))
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Unverified {target.mention}"))

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def blacklist(self, ctx: commands.Context, target: discord.Member):
        data = await self.bot.data.get(target.id)
        action = not data.blacklisted
        await self.bot.data.set(target.id, "blacklisted", action)
        await self.logs.send(embed=discord.Embed(
            title="Member Blacklisted" if action else "Member Unblacklisted",
            color=discord.Color.red() if action else discord.Color.green(),
            timestamp=ctx.message.created_at,
        ).add_field(
            name="Member",
            value=f"{target.mention} ({target}) [{target}]"
        ).add_field(
            name="Moderator",
            value=ctx.author.mention
        ))
        return await ctx.reply(embed=self.bot.static.embed(ctx,
                                                           f"Blacklisted {target.mention}" if action else f"Unblacklisted {target.mention}"))

    async def _verify(self, target: discord.Member, player):
        try:
            guild = await self.bot.hypixel.guild.get(uuid=player.uuid)
        except hypixelaPY.NoGuildFoundError:
            guild = None
        index = player.bedwars.prestige.star_index
        index = 30 if player.bedwars.prestige.star_index > 30 else index
        role = self.bot.prestiges.all[index]
        if not role.role: role.get(self.guild)
        star = player.bedwars.prestige.star
        if len(str(star)) == 1:
            star = f"0{star}"
        await target.edit(nick=f"[{star} {role.star}] {player.name}")
        if role.role not in target.roles:
            for old in self.bot.prestiges.all:
                if not old.role: old.get(self.guild)
                if old.role in target.roles: await target.remove_roles(old)
        await target.add_roles(role.role)
        if guild:
            if guild_role := self.guild_roles.get(guild.id):
                await target.add_roles(guild_role)
        if staff := self.hypixel_roles["STAFF"].get(player.rank.name):
            await target.add_roles(self.hypixel_roles["STAFF"].get("STAFF"))
            await target.add_roles(staff)
        if other := self.hypixel_roles.get(player.rank.name):
            await target.add_roles(other)
        await target.remove_roles(self.need_username_role)

    async def _unverify(self, target: discord.Member):
        for role in self.bot.prestiges.all:
            if not role.role: role.get(self.guild)
            if role.role in target.roles: await target.remove_roles(role.role)
        for role in self.guild_roles.values():
            if role in target.roles: await target.remove_roles(role)
        for role in self.hypixel_roles["STAFF"].values():
            if role in target.roles: await target.remove_roles(role)
        for role in self.hypixel_roles.values():
            if role in target.roles: await target.remove_roles(role)
        await target.add_roles(self.need_username_role)
        await target.edit(nick=None)

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(guild_check)
    @commands.has_role(ROLES.get("STAFF"))
    async def vcs(self, ctx: commands.Context, limit=100):
        result = []
        async for message in self.verification.history(limit=limit):
            words = message.content.split(" ")
            if len(words) < 2: continue
            if words[0] == "r.bwverify" or words[0] == "r.verify":
                result.append(message)
        if not result:
            return await ctx.reply(embed=self.bot.static.embed(ctx, "No verification attemps found!"))
        result = [f"{message.author.mention}: {message.content}" for message in result]
        await menus.MenuPages(source=self.bot.static.paginators.regular(result, ctx, discord.Embed(
            title="Verification Attemps",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        ))).start(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.is_ready or not message.guild or message.guild.id != GUILD_ID: return
        if last := self.auto.get(message.author.id):
            if time.time() - last < TIME_BETWEEN_AUTO:
                return
        user = await self.bot.data.get(message.author.id)
        if not user or not bool(user.uuid): return
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        try:
            await self._verify(message.author, player)
            await self.logs.send(embed=discord.Embed(
                title="Member Updated (On Message)",
                color=discord.Color.green(),
                timestamp=message.created_at,
            ).add_field(
                name="Member",
                value=f"{message.author.mention} ({message.author}) [{message.author.id}]"
            ).add_field(
                name="Moderator",
                value=message.guild.me.mention
            ).add_field(
                name="Minecraft Account",
                value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
            ))
        except discord.Forbidden:
            pass
        self.auto[message.author.id] = time.time()


def setup(bot):
    bot.add_cog(Bedwars(bot))
    print("Reloaded cogs.bedwars")
