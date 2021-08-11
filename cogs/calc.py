import json
from math import ceil
from statistics import mean

import util.bits as bits
from discord import Embed
from discord.ext import commands
from util.config import footer_text, lbin_footer_text
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
        embed.set_footer(**footer_text)

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
        embed.set_footer(**footer_text)

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
            try:
                required = slayerdiff(start, end, type.lower())
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
            elif type in ["wolf", "sven", "s", "enderman", "eman", "e", "voidgloom", "v"]:
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
            else:
                await ctx.reply(
                    f"Hmm, you didn't specify whether or not Aatrox is active properly.\neg `{ctx.prefix}csl 2 5 rev a`"
                )
                return

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
            embed.set_footer(**footer_text)

            await ctx.reply(embed=embed)

    @commands.command(aliases=["fl", "fragrun", "fr"])
    async def fragloot(self, ctx, runs=None, time=None):
        if runs is None:
            await ctx.reply(
                f"You must specify the number of runs (and optionally time in minutes to finish a run)\neg `{ctx.prefix}fl 10 1.5`"
            )
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

        embed.set_footer(**lbin_footer_text)

        await ctx.reply(embed=embed)

    @commands.command(aliases=["bit", "b"])
    async def bits(self, ctx):
        embed = Embed(title="Bits to coins", colour=ctx.guild.me.color)

        with open("util/lbin/lowestbin.json", "r") as f:
            f = json.load(f)

            GOD_POTION = f["GOD_POTION"]
            KAT_FLOWER = f["KAT_FLOWER"]
            HEAT_CORE = f["HEAT_CORE"]
            HYPER_CATALYST_UPGRADE = f["HYPER_CATALYST_UPGRADE"]
            ULTIMATE_CARROT_CANDY_UPGRADE = f["ULTIMATE_CARROT_CANDY_UPGRADE"]
            COLOSSAL_EXP_BOTTLE_UPGRADE = f["COLOSSAL_EXP_BOTTLE_UPGRADE"]
            JUMBO_BACKPACK_UPGRADE = f["JUMBO_BACKPACK_UPGRADE"]
            MINION_STORAGE_EXPANDER = f["MINION_STORAGE_EXPANDER"]
            HOLOGRAM = f["HOLOGRAM"]
            BUILDERS_WAND = f["BUILDERS_WAND"]
            BLOCK_ZAPPER = f["BLOCK_ZAPPER"]
            BITS_TALISMAN = f["BITS_TALISMAN"]
            AUTOPET_RULES_2 = f["AUTOPET_RULES_2"]
            KISMET_FEATHER = f["KISMET_FEATHER"]

            EXPERTISE = f["ENCHANTED_BOOK-EXPERTISE1"]
            COMPACT = f["ENCHANTED_BOOK-COMPACT1"]
            CULTIVATING = f["ENCHANTED_BOOK-CULTIVATING1"]

            ENRICHMENT_SWAPPER = f["TALISMAN_ENRICHMENT_SWAPPER"]
            ENRICHMENT_DEFENSE = f["TALISMAN_ENRICHMENT_DEFENSE"]
            ENRICHMENT_MAGIC_FIND = f["TALISMAN_ENRICHMENT_MAGIC_FIND"]
            ENRICHMENT_FEROCITY = f["TALISMAN_ENRICHMENT_FEROCITY"]
            ENRICHMENT_CRITICAL_DAMAGE = f["TALISMAN_ENRICHMENT_CRITICAL_DAMAGE"]
            ENRICHMENT_CRITICAL_CHANCE = f["TALISMAN_ENRICHMENT_CRITICAL_CHANCE"]
            ENRICHMENT_WALK_SPEED = f["TALISMAN_ENRICHMENT_WALK_SPEED"]
            ENRICHMENT_ATTACK_SPEED = f["TALISMAN_ENRICHMENT_ATTACK_SPEED"]
            ENRICHMENT_HEALTH = f["TALISMAN_ENRICHMENT_HEALTH"]
            ENRICHMENT_INTELLIGENCE = f["TALISMAN_ENRICHMENT_INTELLIGENCE"]
            ENRICHMENT_SEA_CREATURE_CHANCE = f[
                "TALISMAN_ENRICHMENT_SEA_CREATURE_CHANCE"
            ]
            ENRICHMENT_STRENGTH = f["TALISMAN_ENRICHMENT_STRENGTH"]

        god_potion = round(GOD_POTION / bits.god_potion)
        kat_flower = round(KAT_FLOWER / bits.kat_flower)
        heat_core = round(HEAT_CORE / bits.heat_core)
        hyper_catalyst_upgrade = round(
            HYPER_CATALYST_UPGRADE / bits.hyper_catalyst_upgrade
        )
        ultimate_carrot_candy_upgrade = round(
            ULTIMATE_CARROT_CANDY_UPGRADE / bits.ultimate_carrot_candy_upgrade
        )
        colossal_exp_bottle_upgrade = round(
            COLOSSAL_EXP_BOTTLE_UPGRADE / bits.colossal_exp_bottle_upgrade
        )
        jumbo_backpack_upgrade = round(
            JUMBO_BACKPACK_UPGRADE / bits.jumbo_backpack_upgrade
        )
        minion_storage_expander = round(
            MINION_STORAGE_EXPANDER / bits.minion_storage_expander
        )
        hologram = round(HOLOGRAM / bits.hologram)
        builders_wand = round(BUILDERS_WAND / bits.builders_wand)
        block_zapper = round(BLOCK_ZAPPER / bits.block_zapper)
        bits_talisman = round(BITS_TALISMAN / bits.bits_talisman)
        autopet_rules_2 = round(AUTOPET_RULES_2 / bits.autopet_rules_2)
        kismet_feather = round(KISMET_FEATHER / bits.kismet_feather)

        expertise = round(EXPERTISE / bits.books)
        compact = round(COMPACT / bits.books)
        cultivating = round(CULTIVATING / bits.books)

        enrichment_swapper = round(
            ENRICHMENT_SWAPPER / bits.talisman_enrichment_swapper
        )
        enrichment_defense = round(ENRICHMENT_DEFENSE / bits.enrichments)
        enrichment_magic_find = round(ENRICHMENT_MAGIC_FIND / bits.enrichments)
        enrichment_ferocity = round(ENRICHMENT_FEROCITY / bits.enrichments)
        enrichment_critical_damage = round(
            ENRICHMENT_CRITICAL_DAMAGE / bits.enrichments
        )
        enrichment_critical_chance = round(
            ENRICHMENT_CRITICAL_CHANCE / bits.enrichments
        )
        enrichment_walk_speed = round(ENRICHMENT_WALK_SPEED / bits.enrichments)
        enrichment_attack_speed = round(ENRICHMENT_ATTACK_SPEED / bits.enrichments)
        enrichment_health = round(ENRICHMENT_HEALTH / bits.enrichments)
        enrichment_intelligence = round(ENRICHMENT_INTELLIGENCE / bits.enrichments)
        enrichment_sea_creature_chance = round(
            ENRICHMENT_SEA_CREATURE_CHANCE / bits.enrichments
        )
        enrichment_strength = round(ENRICHMENT_STRENGTH / bits.enrichments)

        enrichment_average = round(
            mean(
                [
                    enrichment_defense,
                    enrichment_magic_find,
                    enrichment_ferocity,
                    enrichment_critical_damage,
                    enrichment_critical_chance,
                    enrichment_walk_speed,
                    enrichment_attack_speed,
                    enrichment_health,
                    enrichment_intelligence,
                    enrichment_sea_creature_chance,
                    enrichment_strength,
                ]
            )
        )

        embed.add_field(name="God Potion", value=f"{god_potion} coins per bit")
        embed.add_field(name="Kat Flower", value=f"{kat_flower} coins per bit")
        embed.add_field(name="Heat Core", value=f"{heat_core} coins per bit")
        embed.add_field(
            name="Hyper Catalyst Upgrade",
            value=f"{hyper_catalyst_upgrade} coins per bit",
        )
        embed.add_field(
            name="Ultimate Carrot Candy",
            value=f"{ultimate_carrot_candy_upgrade} coins per bit",
        )
        embed.add_field(
            name="Colossal XP Bottle",
            value=f"{colossal_exp_bottle_upgrade} coins per bit",
        )
        embed.add_field(
            name="Jumbo BP", value=f"{jumbo_backpack_upgrade} coins per bit"
        )
        embed.add_field(
            name="Minion Storage Expander",
            value=f"{minion_storage_expander} coins per bit",
        )
        embed.add_field(name="Hologram", value=f"{hologram} coins per bit")
        embed.add_field(name="Builder's Wand", value=f"{builders_wand} coins per bit")
        embed.add_field(name="Block Zapper", value=f"{block_zapper} coins per bit")
        embed.add_field(name="Bits Talisman", value=f"{bits_talisman} coins per bit")
        embed.add_field(name="AutoPet Rule", value=f"{autopet_rules_2} coins per bit")
        embed.add_field(name="Kismet Feather", value=f"{kismet_feather} coins per bit")
        embed.add_field(name="Expertise Book", value=f"{expertise} coins per bit")
        embed.add_field(name="Compact Book", value=f"{compact} coins per bit")
        embed.add_field(name="Cultivating Book", value=f"{cultivating} coins per bit")
        embed.add_field(
            name="Enrichment Swapper", value=f"{enrichment_swapper} coins per bit"
        )
        embed.add_field(
            name="All enrichments (average)",
            value=f"{enrichment_average} coins per bit",
        )

        embed.set_footer(**lbin_footer_text)

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Calc(bot))
