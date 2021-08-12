from commands import fragrun, bits
from commands import calc
from discord.ext import commands


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cc"])
    async def calccata(self, ctx, start=None, end=None, xp=None):
        if start is None or end is None:
            await ctx.reply(
                f"You must enter the current and desired Catacombs level! (and optionally how much xp you get from each run)\neg `{ctx.prefix}cc 1 10 10,000`"
            )
        elif not start.isnumeric() or not end.isnumeric():
            await ctx.reply(
                "That doesn't seem like a valid number. Remove any non-digit!"
            )
        else:
            embed = calc.calccata(ctx, start, end, xp)
            if embed == IndexError:
                await ctx.reply(
                    f"The skill level must be from 0-60!\neg `{ctx.prefix}cs 1 10`"
                )
            else:
                await ctx.reply(embed=embed)

    @commands.command(aliases=["cs"])
    async def calcskill(self, ctx, start=None, end=None):
        if start is None or end is None:
            await ctx.reply(
                f"You must enter the current and desired skill level!\neg `{ctx.prefix}cs 1 10`"
            )
        elif not start.isnumeric() or not end.isnumeric():
            await ctx.reply(
                "That doesn't seem like a valid number. Remove any non-digit!"
            )
        else:
            embed = calc.calcskill(ctx, start, end)
            if embed == IndexError:
                await ctx.reply(
                    f"The skill level must be from 0-60!\neg `{ctx.prefix}cs 1 10`"
                )
            else:
                await ctx.reply(embed=embed)

    @commands.command(aliases=["csl"])
    async def calcslayer(self, ctx, start=None, end=None, type=None, aatrox=None):
        if start is None or end is None:
            await ctx.reply(
                f"You must enter the current and desired slayer level, and the type (and optionally Aatrox perk)!\neg `{ctx.prefix}csl 2 5 rev aatrox`"
            )
        elif not start.isnumeric() or not end.isnumeric():
            await ctx.reply(
                "That doesn't seem like a valid number. Remove any non-digit!"
            )
        elif type is None:
            await ctx.send(
                f"You must specify the slayer type!\neg `{ctx.prefix}csl 2 5 rev`"
            )
        else:
            embed = calc.calcslayer(ctx, start, end, type, aatrox)
            if embed == IndexError:
                await ctx.reply(
                    f"You must enter the current and desired slayer level from 0 to 9, and the type!\neg `{ctx.prefix}csl 2 5 rev`"
                )
            elif embed == "SlayerError":
                await ctx.reply(
                    f"That's not a valid slayer type!\neg `{ctx.prefix}csl 2 5 rev/tara/sven/eman`"
                )
            elif embed == "AatroxError":
                await ctx.reply(
                    f"Hmm, you didn't specify whether or not Aatrox is active properly.\neg `{ctx.prefix}csl 2 5 rev aatrox`"
                )
            else:
                await ctx.reply(embed=embed)

    @commands.command(aliases=["fl", "fragrun", "fr"])
    async def fragloot(self, ctx, runs=None, time=None):
        if runs is None:
            await ctx.reply(
                f"You must specify the number of runs (and optionally time in minutes to finish a run)\neg `{ctx.prefix}fl 10 1.5`"
            )
        else:
            runs = runs.replace(",", "")
            if not runs.isnumeric():
                await ctx.reply(
                    "Runs must be a valid integer! Remove anything that is not a comma or a number."
                )
            elif time is not None:
                try:
                    time = float(time)
                except ValueError:
                    return await ctx.reply(
                        "Time must be a valid number! Remove anything that is not a decimal or a number."
                    )

                embed = fragrun.fragrun(ctx, int(runs), time)
                await ctx.reply(embed=embed)

    @commands.command(aliases=["bit", "b"])
    async def bits(self, ctx):
        embed = bits.bits(ctx)
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
