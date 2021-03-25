import time

from discord.ext import commands, menus
import discord

import hypixelaPY

import static

TIME_BETWEEN_AUTO = 86400  # 24 hours in seconds


class Bedwars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto = {}

    @commands.command(aliases=["v", "bwverify"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(static.guild_check)
    @commands.check(static.verification_check)
    async def verify(self, ctx: commands.Context, query: str):
        if user := await self.bot.data.get(ctx.author.id):
            if bool(user.uuid):
                await self.bot.static.channels.logs.send(embed=discord.Embed(
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
                return await ctx.reply(embed=self.bot.static.embed(ctx, "You are already verified! Type `r.u` to "
                                                                        "update!"))
            elif user.blacklisted:
                await self.bot.static.channels.logs.send(embed=discord.Embed(
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
            await self.bot.static.channels.logs.send(embed=discord.Embed(
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
            return await ctx.reply(
                embed=self.bot.static.embed(ctx, f"You have not linked your Discord tag on Hypixel!\n"
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
            await self.bot.static.channels.logs.send(embed=discord.Embed(
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
        await self.bot.static.channels.logs.send(embed=discord.Embed(
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
        return await ctx.message.delete()

    @commands.command(aliases=["bwupdate", "u"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(static.guild_check)
    @commands.check(static.update_check)
    async def update(self, ctx: commands.Context):
        user = await self.bot.data.get(ctx.author.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, "You are not verified! Verify first with "
                                                                    "`r.verify <your-ign>`"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(ctx.author, player)
        await self.bot.static.channels.logs.send(embed=discord.Embed(
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
    @commands.check(static.guild_check)
    @commands.has_role(static.STAFF_ROLE_ID)
    async def forceupdate(self, ctx: commands.Context, target: discord.Member):
        user = await self.bot.data.get(target.id)
        if not user or not bool(user.uuid):
            return await ctx.reply(embed=self.bot.static.embed(ctx, f"{target.mention} is not verified!"))
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        await self._verify(target, player)
        await self.bot.static.channels.logs.send(embed=discord.Embed(
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
    @commands.check(static.guild_check)
    @commands.has_role(static.STAFF_ROLE_ID)
    async def forceverify(self, ctx: commands.Context, target: discord.Member, query: str):
        player = await self.bot.hypixel.player.get(query=query)
        await self.bot.data.set(target.id, "uuid", player.uuid)
        await self._verify(target, player)
        await self.bot.static.channels.logs.send(embed=discord.Embed(
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
        return await ctx.message.delete()

    @commands.command(aliases=["forceunverify", "uv", "fuv"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(static.guild_check)
    @commands.has_role(static.STAFF_ROLE_ID)
    async def unverify(self, ctx: commands.Context, target: discord.Member):
        data = await self.bot.data.get(target.id)
        if not data or not bool(data.uuid): return await ctx.reply(
            embed=self.bot.static.embed(ctx, f"{target.mention} was not verified!"))
        await self.bot.data.set(target.id, "uuid", None)
        await self._unverify(target)
        await self.bot.static.channels.logs.send(embed=discord.Embed(
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
    @commands.check(static.guild_check)
    @commands.has_role(static.STAFF_ROLE_ID)
    async def blacklist(self, ctx: commands.Context, target: discord.Member):
        data = await self.bot.data.get(target.id)
        action = not data.blacklisted
        await self.bot.data.set(target.id, "blacklisted", action)
        await self.bot.static.channels.logs.send(embed=discord.Embed(
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
        return await ctx.reply(
            embed=self.bot.static.embed(ctx,
                                        f"Blacklisted {target.mention}" if action else f"Unblacklisted {target.mention}"
                                        ))

    async def _verify(self, target: discord.Member, player):
        try:
            guild = await self.bot.hypixel.guild.get(uuid=player.uuid)
        except hypixelaPY.NoGuildFoundError:
            guild = None
        index = player.bedwars.prestige.star_index
        index = 30 if player.bedwars.prestige.star_index > 30 else index
        # current highest prestige is 3000, then it's the same
        role = self.bot.prestiges.all[index]
        if not role.role: role.get(self.bot.static.guild)
        star = player.bedwars.prestige.star
        if len(str(star)) == 1:
            star = f"0{star}"
        await target.edit(nick=f"[{star} {role.star}] {player.name}")
        if role.role not in target.roles:
            for old in self.bot.prestiges.all:
                if not old.role: old.get(self.bot.static.guild)
                if old.role in target.roles: await target.remove_roles(old)
        await target.add_roles(role.role)
        if guild:
            if guild_role := self.bot.static.roles.guilds.dict.get(guild.id):
                await target.add_roles(guild_role)
        if hypixel_role := self.bot.static.roles.hypixel.dict.get(player.rank.name):
            if player.rank.name in ["MOD", "ADMIN"]:
                await target.add_roles(self.bot.static.roles.hypixel.staff)
            await target.add_roles(hypixel_role)
        await target.remove_roles(self.bot.static.roles.need_username)
        await target.remove_roles(self.bot.static.roles.need_usernames)
        await self.bot.static.channels.verification.purge(check=lambda m: m.author.id == target.id)

    async def _unverify(self, target: discord.Member):
        for role in self.bot.prestiges.all:
            if not role.role: role.get(self.bot.static.guild)
            if role.role in target.roles: await target.remove_roles(role.role)
        for guild_role in self.bot.static.roles.guilds.dict.values():
            if guild_role in target.roles: await target.remove_roles(guild_role)
        for hypixel_role in self.bot.static.roles.hypixel.dict.values():
            if hypixel_role in target.roles: await target.remove_roles(hypixel_role)
        await target.add_roles(self.bot.static.roles.need_username)
        await target.edit(nick=None)

    @commands.command(aliases=["vcs"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(static.guild_check)
    @commands.has_role(static.STAFF_ROLE_ID)
    async def verificationchannelscan(self, ctx: commands.Context, limit=100):
        result = []
        async for message in self.bot.static.channels.verification.history(limit=limit):
            if message.author not in ctx.guild.members: continue
            words = message.content.split(" ")
            if len(words) < 2: continue
            data = await self.bot.data.get(message.author.id)
            if data and bool(data.uuid): continue
            if words[0].lower() in ["r.verify", "r.bwverify", "r.v"] and words[1].lower() not in ["ign", "litelt"]:
                result.append(message)
        if not result:
            return await ctx.reply(embed=self.bot.static.embed(ctx, "No verification attemps found!"))
        result = [f"{message.author.mention} ({message.author.nick}): `{message.content}` ({message.id})" for message in result]
        print("\n".join(result))
        await menus.MenuPages(source=self.bot.static.paginators.regular(result, ctx, discord.Embed(
            title="Verification Attemps",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        ))).start(ctx)

    @commands.command(aliases=["fvm"])
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @commands.check(static.guild_check)
    @commands.has_role(static.STAFF_ROLE_ID)
    async def forceverifymessage(self, ctx: commands.Context, message: discord.Message):
        words = message.content.split(" ")
        if len(words) < 2: return await ctx.reply(embed=self.bot.static.embed(ctx, "Less than two words in message, "
                                                                                   "skipping"))
        if not words[0].lower() in ["r.verify", "r.bwverify", "r.v"]:
            return await ctx.reply(
                embed=self.bot.static.embed(ctx, "Not a verification attempt!"))
        player = await self.bot.hypixel.player.get(query=words[1])
        await self.bot.data.set(message.author.id, "uuid", player.uuid)
        await self._verify(message.author, player)
        await self.bot.static.channels.logs.send(embed=discord.Embed(
            title="Member Force Verified (From User Verify Attempt)",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at
        ).add_field(
            name="Member",
            value=f"{message.author.mention} ({message.author}) [{message.author.id}]"
        ).add_field(
            name="Moderator",
            value=ctx.author.mention
        ).add_field(
            name="Minecraft Account",
            value=f"[{player.name}]({self.bot.static.plancke_url(player.uuid)})"
        ))
        await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified {message.author.mention} as {player}"),
                        delete_after=5)
        await ctx.message.delete()
        return await self.bot.static.channels.verification.purge(check=lambda m: m.author.id == message.author.id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.is_ready() or not message.guild or message.guild != self.bot.static.guild: return
        if last := self.auto.get(message.author.id):
            if time.time() - last < TIME_BETWEEN_AUTO:
                return
        user = await self.bot.data.get(message.author.id)
        if not user or not bool(user.uuid): return
        player = await self.bot.hypixel.player.get(uuid=user.uuid)
        try:
            await self._verify(message.author, player)
            await self.bot.static.channels.logs.send(embed=discord.Embed(
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
