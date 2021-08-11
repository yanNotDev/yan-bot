import json
from math import ceil
from statistics import mean

import util.bits as bits
from bot import slash_blacklist
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from util.config import footer_text, lbin_footer_text
from util.skill import catadiff, lvdiff, slayerdiff


class SlashCalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description="Checks xp required to get from one Catacombs level to another.",
        # guild_ids=guilds,
        options=[
            create_option("start", "Starting level", 4, True),
            create_option("end", "Ending level", 4, True),
            create_option("xp", "XP per floor", 10, False),
        ],
    )
    async def calccata(self, ctx, start, end, xp=None):
        try:
            required_int = catadiff(start, end)
        except IndexError:
            await ctx.send("You can't enter a level higher than 50!", hidden=True)
            return

        required = "{:,}".format(required_int)

        embed = Embed(
            description=f"{required} xp is required to get from Catacombs {start} to {end}.",
            colour=ctx.guild.me.color,
        )
        if xp is not None:
            runs = "{:,}".format(ceil(required_int / xp))
            embed.add_field(name=f"Runs required to reach Catacombs {end}", value=runs)
        embed.set_footer(**footer_text)

        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Checks xp required to get from one level to another, for the 7 main skills.",
        # guild_ids=guilds,
        options=[
            create_option("start", "Starting level", 4, True),
            create_option("end", "Ending level", 4, True),
        ],
    )
    async def calcskill(self, ctx, start, end):
        try:
            required = "{:,}".format(lvdiff(start, end))
        except IndexError:
            await ctx.send("You can't enter a level higher than 60!", hidden=True)
            return

        embed = Embed(
            description=f"{required} xp is required to get from Level {start} to {end}.",
            colour=ctx.guild.me.color,
        )
        embed.set_footer(**footer_text)

        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Checks xp required to get from one slayer level to another.",
        # guild_ids=guilds,
        options=[
            create_option("start", "Starting level", 4, True),
            create_option("end", "Ending level", 4, True),
            create_option(
                "type",
                "Type",
                3,
                True,
                choices=[
                    create_choice("Revenant", "Revenant"),
                    create_choice("Tarantula", "Tarantula"),
                    create_choice("Sven/Voidgloom", "Sven/Voidgloom"),
                ],
            ),
            create_option("aatrox", "Is Aatrox active", 5, False),
        ],
    )
    async def calcslayer(self, ctx, start, end, type, aatrox=False):
        try:
            required = slayerdiff(start, end, type)
        except IndexError:
            await ctx.send("Slayer level can only be from 0 to 9!", hidden=True)
            return

        required_str = "{:,}".format(required)

        if not aatrox:
            t1_xp, t1_cost = 5, 2000
            t2_xp, t2_cost = 25, 7500
            t3_xp, t3_cost = 100, 20000
            t4_xp, t4_cost = 500, 50000
            t5_xp, t5_cost = 1500, 100000
        elif aatrox:
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
        embed.set_footer(**footer_text)

        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Calculates average profit from fragrunning.",
        # guild_ids=guilds,
        options=[
            create_option("runs", "Number of fragruns", 4, True),
            create_option("time", "Time in minutes to finish 1 fragrun", 10, False),
        ],
    )
    async def fragloot(self, ctx, runs, time=None):
        if runs == 1:
            embed = Embed(
                title="Average loot from one fragrun", colour=ctx.guild.me.color
            )
        else:
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

        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Calculates coins per bit for all auctionable items.",
        # guild_ids=guilds
    )
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

        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)


def setup(bot: commands.Bot):
    bot.add_cog(SlashCalc(bot))
