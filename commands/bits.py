import json
from discord import Embed
from statistics import mean
from util.config import lbin_footer_text


def bits(ctx):
    bits_god_potion = 1500
    bits_kat_flower = 500
    bits_heat_core = 3000
    bits_hyper_catalyst_upgrade = 300
    bits_ultimate_carrot_candy_upgrade = 8000
    bits_colossal_exp_bottle_upgrade = 1200
    bits_jumbo_backpack_upgrade = 4000
    bits_minion_storage_expander = 1500
    bits_hologram = 2000
    bits_builders_wand = 12000
    bits_block_zapper = 5000
    bits_bits_talisman = 15000
    bits_autopet_rules_2 = 21000
    bits_kismet_feather = 1350

    bits_books = 4000

    bits_enrichments = 5000
    bits_talisman_enrichment_swapper = 200

    embed = Embed(title="Bits to coins", colour=ctx.guild.me.color)

    with open("util/lbin/lowestbin.json", "r") as f:
        f = json.load(f)

        GOD_POTION = f.get("GOD_POTION", 0)
        KAT_FLOWER = f.get("KAT_FLOWER", 0)
        HEAT_CORE = f.get("HEAT_CORE", 0)
        HYPER_CATALYST_UPGRADE = f.get("HYPER_CATALYST_UPGRADE", 0)
        ULTIMATE_CARROT_CANDY_UPGRADE = f.get("ULTIMATE_CARROT_CANDY_UPGRADE", 0)
        COLOSSAL_EXP_BOTTLE_UPGRADE = f.get("COLOSSAL_EXP_BOTTLE_UPGRADE", 0)
        JUMBO_BACKPACK_UPGRADE = f.get("JUMBO_BACKPACK_UPGRADE", 0)
        MINION_STORAGE_EXPANDER = f.get("MINION_STORAGE_EXPANDER", 0)
        HOLOGRAM = f.get("HOLOGRAM", 0)
        BUILDERS_WAND = f.get("BUILDERS_WAND", 0)
        BLOCK_ZAPPER = f.get("BLOCK_ZAPPER", 0)
        BITS_TALISMAN = f.get("BITS_TALISMAN", 0)
        AUTOPET_RULES_2 = f.get("AUTOPET_RULES_2", 0)
        KISMET_FEATHER = f.get("KISMET_FEATHER", 0)

        EXPERTISE = f.get("ENCHANTED_BOOK-EXPERTISE1", 0)
        COMPACT = f.get("ENCHANTED_BOOK-COMPACT1", 0)
        CULTIVATING = f.get("ENCHANTED_BOOK-CULTIVATING1", 0)

        ENRICHMENT_SWAPPER = f.get("TALISMAN_ENRICHMENT_SWAPPER", 0)
        ENRICHMENT_DEFENSE = f.get("TALISMAN_ENRICHMENT_DEFENSE", 0)
        ENRICHMENT_MAGIC_FIND = f.get("TALISMAN_ENRICHMENT_MAGIC_FIND", 0)
        ENRICHMENT_FEROCITY = f.get("TALISMAN_ENRICHMENT_FEROCITY", 0)
        ENRICHMENT_CRITICAL_DAMAGE = f.get("TALISMAN_ENRICHMENT_CRITICAL_DAMAGE", 0)
        ENRICHMENT_CRITICAL_CHANCE = f.get("TALISMAN_ENRICHMENT_CRITICAL_CHANCE", 0)
        ENRICHMENT_WALK_SPEED = f.get("TALISMAN_ENRICHMENT_WALK_SPEED", 0)
        ENRICHMENT_ATTACK_SPEED = f.get("TALISMAN_ENRICHMENT_ATTACK_SPEED", 0)
        ENRICHMENT_HEALTH = f.get("TALISMAN_ENRICHMENT_HEALTH", 0)
        ENRICHMENT_INTELLIGENCE = f.get("TALISMAN_ENRICHMENT_INTELLIGENCE", 0)
        ENRICHMENT_SEA_CREATURE_CHANCE = f.get("TALISMAN_ENRICHMENT_SEA_CREATURE_CHANCE", 0)
        ENRICHMENT_STRENGTH = f.get("TALISMAN_ENRICHMENT_STRENGTH", 0)

    god_potion = round(GOD_POTION / bits_god_potion)
    kat_flower = round(KAT_FLOWER / bits_kat_flower)
    heat_core = round(HEAT_CORE / bits_heat_core)
    hyper_catalyst_upgrade = round(HYPER_CATALYST_UPGRADE / bits_hyper_catalyst_upgrade)
    ultimate_carrot_candy_upgrade = round(
        ULTIMATE_CARROT_CANDY_UPGRADE / bits_ultimate_carrot_candy_upgrade
    )
    colossal_exp_bottle_upgrade = round(
        COLOSSAL_EXP_BOTTLE_UPGRADE / bits_colossal_exp_bottle_upgrade
    )
    jumbo_backpack_upgrade = round(JUMBO_BACKPACK_UPGRADE / bits_jumbo_backpack_upgrade)
    minion_storage_expander = round(
        MINION_STORAGE_EXPANDER / bits_minion_storage_expander
    )
    hologram = round(HOLOGRAM / bits_hologram)
    builders_wand = round(BUILDERS_WAND / bits_builders_wand)
    block_zapper = round(BLOCK_ZAPPER / bits_block_zapper)
    bits_talisman = round(BITS_TALISMAN / bits_bits_talisman)
    autopet_rules_2 = round(AUTOPET_RULES_2 / bits_autopet_rules_2)
    kismet_feather = round(KISMET_FEATHER / bits_kismet_feather)

    expertise = round(EXPERTISE / bits_books)
    compact = round(COMPACT / bits_books)
    cultivating = round(CULTIVATING / bits_books)

    enrichment_swapper = round(ENRICHMENT_SWAPPER / bits_talisman_enrichment_swapper)
    enrichment_defense = round(ENRICHMENT_DEFENSE / bits_enrichments)
    enrichment_magic_find = round(ENRICHMENT_MAGIC_FIND / bits_enrichments)
    enrichment_ferocity = round(ENRICHMENT_FEROCITY / bits_enrichments)
    enrichment_critical_damage = round(
        ENRICHMENT_CRITICAL_DAMAGE / bits_enrichments
    )
    enrichment_critical_chance = round(
        ENRICHMENT_CRITICAL_CHANCE / bits_enrichments
    )
    enrichment_walk_speed = round(ENRICHMENT_WALK_SPEED / bits_enrichments)
    enrichment_attack_speed = round(ENRICHMENT_ATTACK_SPEED / bits_enrichments)
    enrichment_health = round(ENRICHMENT_HEALTH / bits_enrichments)
    enrichment_intelligence = round(ENRICHMENT_INTELLIGENCE / bits_enrichments)
    enrichment_sea_creature_chance = round(
        ENRICHMENT_SEA_CREATURE_CHANCE / bits_enrichments
    )
    enrichment_strength = round(ENRICHMENT_STRENGTH / bits_enrichments)

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
    embed.add_field(name="Jumbo BP", value=f"{jumbo_backpack_upgrade} coins per bit")
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
    embed.add_field(
        name="All enrichments (average)",
        value=f"?",
        )
    embed.set_footer(**lbin_footer_text)

    return embed
