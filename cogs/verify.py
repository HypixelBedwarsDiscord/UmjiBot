from discord.ext import commands
import discord


class Verify:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx: commands.Context, query: str):
        if self.bot.data.get(ctx.author.id).blacklisted:
            return await ctx.reply(embed=self.bot.static.embed(ctx, "You are blacklisted from verification!"))
        player = self.bot.hypixel.get(query=query)
        if str(ctx.author) != player.social.discord:
            return await ctx.reply(embed=self.bot.static.embed(ctx, "Set your Discord name and tag on Hypixel first!"))
        self.bot.data.set(ctx.author.id, "uuid", player.uuid)
        await self.set_role(ctx.author, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified you as {player}"))

    @commands.command()
    async def forceverify(self, ctx: commands.Context, target: discord.Member, query: str):
        player = self.bot.hypixel.get(query=query)
        self.bot.data.set(target.id, "uuid", player.uuid)
        await self.set_role(target, player)
        return await ctx.reply(embed=self.bot.static.embed(ctx, f"Verified {target.mention} as {player}"))

    async def set_role(self, target: discord.Member, player):
        role = self.bot.prestiges.get[player.bedwars.prestige.star_index]
        if not role.role: role.get(self.bot)
        await target.add_roles(role)


def setup(bot):
    bot.add_cog(Verify(bot))
    print("Reloaded cogs.verify")
