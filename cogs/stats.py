from commands import stats
from discord import Embed
from discord.ext import commands
from util.config import footer_text
from commands.uuid import uuid


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["s"])
    async def stats(self, ctx, ign=None, profile=None):
        if ign is None:
            return await ctx.reply(
                f"You must enter an ign (and optionally, a profile)!\neg `{ctx.prefix}s minikloon banana`\n\
If you're too lazy to do that, do `{ctx.prefix}help bind`"
            )

        mcuuid = await uuid(self.bot, ctx.author.id, ign)
        if mcuuid == 204:
            await ctx.reply("Invalid IGN!")
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, sorry :cry:",
                colour=ctx.guild.me.color,
            )
            embed.add_field(
                name="HYPIXEL WHY are you so sLOW", value="_ _", inline=False
            )
            embed.set_footer(**footer_text)
            msg = await ctx.reply(embed=embed)

            embed = stats.stats(ctx, mcuuid, profile)
            await msg.edit(embed=embed)

    @commands.command(aliases=["uuid"])
    async def mcuuid(self, ctx, ign=None):
        id = await uuid(self.bot, ctx.author.id, ign)
        if id == 204:
            await ctx.reply("Invalid IGN!")
        elif id == KeyError:
            await ctx.reply(
                f"You must enter an ign!\neg `{ctx.prefix}uuid minikloon`\n\
If you're too lazy to do that, do `{ctx.prefix}help link`"
            )
        else:
            if ign is None:
                msg = f"You have the UUID `{id}`"
            else:
                msg = f"{ign} has the UUID `{id}`"
            await ctx.reply(msg)


def setup(bot: commands.Bot):
    bot.add_cog(Stats(bot))
