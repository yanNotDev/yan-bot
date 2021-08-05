from bot import blc
import json
from math import ceil

from discord import Embed
from discord.ext import commands
from util.skill import catadiff, lvdiff, slayerdiff


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cc"])
    async def calccata(self, ctx, start=None, end=None, xp=None):
        try:
            if start is None or end is None:
                await ctx.reply(
                    f"You must enter the current and desired Catacombs level! (and optionally how much xp you get from each run)\neg `{ctx.prefix}cc 1 10 10,000`"
                )
                return
            if start.isnumeric() is False or end.isnumeric() is False:
                await ctx.reply(
                    "That doesn't seem like a valid number. Remove any non-digit!"
                )
                return
            required_int = catadiff(start, end)
        except IndexError:
            await ctx.reply(
                f"You must enter the current and desired Catacombs level from 0 to 50! (and optionally how much xp you get from each run)\neg `{ctx.prefix}cc 1 10 10,000`"
            )
            return

        required = "{:,}".format(required_int)

        embed = Embed(
            description=f"{required} xp is required to get from Catacombs {start} to {end}.",
            colour=ctx.guild.me.color,
        )
        if xp is not None:
            try:
                runs = "{:,}".format(ceil(required_int / float(xp.replace(",", ""))))
            except ValueError:
                await ctx.reply(
                    "That doesn't seem like a valid number. Remove any letters!"
                )
            embed.add_field(name=f"Runs required to reach Catacombs {end}", value=runs)
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.reply(embed=embed)

    @commands.command(aliases=["cs"])
    async def calcskill(self, ctx, start=None, end=None):
        try:
            if start is None or end is None:
                await ctx.reply(
                    f"You must enter the current and desired skill level!\neg `{ctx.prefix}cs 1 10`"
                )
                return
            if start.isnumeric() is False or end.isnumeric() is False:
                await ctx.reply(
                    "That doesn't seem like a valid number. Remove any non-digit!"
                )
                return
            required = "{:,}".format(lvdiff(start, end))
        except IndexError:
            await ctx.reply(
                f"You must enter the current and desired skill level from 0 to 60!\neg `{ctx.prefix}cs 1 10`"
            )
            return

        embed = Embed(
            description=f"{required} xp is required to get from Level {start} to {end}.",
            colour=ctx.guild.me.color,
        )
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.reply(embed=embed)

    @commands.command(aliases=["csl"])
    async def calcslayer(self, ctx, start=None, end=None, type=None, aatrox=None):
        try:
            if start is None or end is None:
                await ctx.reply(
                    f"You must enter the current and desired slayer level, and the type (and optionally Aatrox perk)!\neg `{ctx.prefix}csl 2 5 rev aatrox`"
                )
                return
            if start.isnumeric() is False or end.isnumeric() is False:
                await ctx.reply(
                    "That doesn't seem like a valid number. Remove any non-digit!"
                )
                return
            required = slayerdiff(start, end, type)
        except IndexError:
            await ctx.reply(
                f"You must enter the current and desired slayer level from 0 to 9, and the type!\neg `{ctx.prefix}csl 2 5 rev`"
            )
            return
        if required == "SlayerError":
            await ctx.reply(
                f"That's not a valid slayer type!\neg `{ctx.prefix}csl 2 5 rev/tara/sven/eman`"
            )
            return

        required_str = "{:,}".format(required)

        if type in ["zombie", "revenant", "rev", "r"]:
            type = "Revenant"
        elif type in ["spider", "tarantula", "tara", "t"]:
            type = "Tarantula"
        elif type in ["wolf", "sven", "s", "enderman", "eman", "e", "voidbloom", "v"]:
            type = "Sven/Enderman"

        if aatrox is None or aatrox.lower() in ["false", "f", "no", "n"]:
            t1_xp, t1_cost = 5, 2000
            t2_xp, t2_cost = 25, 7500
            t3_xp, t3_cost = 100, 20000
            t4_xp, t4_cost = 500, 50000
            t5_xp, t5_cost = 1500, 100000
        elif aatrox.lower() in ["true", "t", "yes", "y", "aatrox", "a"]:
            t1_xp, t1_cost = 6.25, 1000
            t2_xp, t2_cost = 31.25, 3750
            t3_xp, t3_cost = 125, 10000
            t4_xp, t4_cost = 625, 25000
            t5_xp, t5_cost = 1875, 50000

        embed = Embed(
            description=f"{required_str} xp is required to get from {type} {start} to {end}.",
            colour=ctx.guild.me.color,
        )

        t1 = ceil(required / t1_xp)
        t1_total_cost = "{:,}".format(t1 * t1_cost)

        t2 = ceil(required / t2_xp)
        t2_total_cost = "{:,}".format(t2 * t2_cost)

        t3 = ceil(required / t3_xp)
        t3_total_cost = "{:,}".format(t3 * t3_cost)

        t4 = ceil(required / t4_xp)
        t4_total_cost = "{:,}".format(t4 * t4_cost)

        embed.add_field(name="T1", value=f"{t1} ({t1_total_cost} coins)", inline=False)
        embed.add_field(name="T2", value=f"{t2} ({t2_total_cost} coins)", inline=False)
        embed.add_field(name="T3", value=f"{t3} ({t3_total_cost} coins)", inline=False)
        embed.add_field(name="T4", value=f"{t4} ({t4_total_cost} coins)", inline=False)
        if type == "Revenant":
            t5 = ceil(required / t5_xp)
            t5_total_cost = "{:,}".format(t5 * t5_cost)
            embed.add_field(
                name="T5", value=f"{t5} ({t5_total_cost} coins)", inline=False
            )
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.reply(embed=embed)

    @commands.command(aliases=["fl", "fragrun", "fr"])
    @commands.check(blc)
    async def fragloot(self, ctx, runs=1, time=None):
        if runs == 1:
            embed = Embed(
                title="Average loot from one fragrun", colour=ctx.guild.me.color
            )
        else:
            try:
                runs = int(runs)
            except ValueError:
                await ctx.reply(f"That's not a valid number!\neg `{ctx.prefix}fl 10`")
                return
            embed = Embed(
                title=f"Average loot from {runs} fragruns", colour=ctx.guild.me.color
            )

        runs = runs / 8

        with open("util/lbin/lowestbin.json", "r") as f:
            f = json.load(f)
            HANDLE = f["GIANT_FRAGMENT_DIAMOND"]
            ROCK = f["GIANT_FRAGMENT_BOULDER"]
            LASR = f["GIANT_FRAGMENT_LASER"]
            LASSO = f["GIANT_FRAGMENT_BIGFOOT"]

        handle_profit = round(HANDLE * runs)
        rock_profit = round(ROCK * runs)
        lasr_profit = round(LASR * runs)
        lasso_profit = round(LASSO * runs)

        total_profit = handle_profit + rock_profit + lasr_profit + lasso_profit
        if time is not None:
            try:
                time = float(time)
            except ValueError:
                await ctx.reply(
                    f"You must enter a valid time in minutes!\neg `{ctx.prefix}fl 10 2.5`"
                )
                return

            profit_per_hour = "{:,}".format(
                round((HANDLE / 8 + ROCK / 8 + LASR / 8 + LASSO / 8) * 60 / time)
            )
            embed.add_field(
                name="Coins per hour", value=f"{profit_per_hour}/hour", inline=False
            )

        total_profit = "{:,}".format(total_profit)
        handle_profit = "{:,}".format(handle_profit)
        rock_profit = "{:,}".format(rock_profit)
        lasr_profit = "{:,}".format(lasr_profit)
        lasso_profit = "{:,}".format(lasso_profit)

        embed.add_field(
            name="Diamante's Handle", value=f"x{runs} ({handle_profit} coins)"
        )
        embed.add_field(name="Jolly Pink Rock", value=f"x{runs} ({rock_profit} coins)")
        embed.add_field(name="L.A.S.R.'s Eye", value=f"x{runs} ({lasr_profit} coins)")
        embed.add_field(name="Bigfoot's Lasso", value=f"x{runs} ({lasso_profit} coins)")
        embed.add_field(name="Total", value=f"{total_profit} coins")

        embed.set_footer(
            text="Made by yan#0069 • Lowest BINs update every 2 minutes",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
