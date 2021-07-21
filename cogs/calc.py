from discord.ext import commands
from discord import Embed
from math import ceil
from util.skill import catadiff, lvdiff


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cc"])
    async def calccata(self, ctx, start, end, xp=None):
        required_int = catadiff(start, end)
        required = "{:,}".format(required_int)

        embed = Embed(
            description=f"{required} xp is required to get from Catacombs {start} to {end}.",
            colour=ctx.guild.me.color,
        )
        if xp is not None:
            runs = "{:,}".format(ceil(required_int / int(xp)))
            embed.add_field(name=f"Runs required to reach Catacombs {end}", value=runs)
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["cs"])
    async def calcskill(self, ctx, start, end):
        required = "{:,}".format(lvdiff(start, end))

        embed = Embed(
            description=f"{required} xp is required to get from Level {start} to {end}.",
            colour=ctx.guild.me.color,
        )
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
