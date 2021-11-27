from math import log10
from re import sub

import requests
from discord import Embed
from util.config import footer_text, key


def lvcheck(xp, cap):
    table = [
        50,
        125,
        200,
        300,
        500,
        750,
        1000,
        1500,
        2000,
        3500,
        5000,
        7500,
        10000,
        15000,
        20000,
        30000,
        50000,
        75000,
        100000,
        200000,
        300000,
        400000,
        500000,
        600000,
        700000,
        800000,
        900000,
        1000000,
        1100000,
        1200000,
        1300000,
        1400000,
        1500000,
        1600000,
        1700000,
        1800000,
        1900000,
        2000000,
        2100000,
        2200000,
        2300000,
        2400000,
        2500000,
        2600000,
        2750000,
        2900000,
        3100000,
        3400000,
        3700000,
        4000000,
        4300000,
        4600000,
        4900000,
        5200000,
        5500000,
        5800000,
        6100000,
        6400000,
        6700000,
        7000000,
    ]
    lv = 0
    needed = 0
    for x in table:
        needed += x
    for x in table:
        if xp - x > 0:
            xp -= x
            lv += 1
        else:
            break
    lv = min(lv, cap)
    return lv


def crops(r, mcuuid, inv, crop):
    if crop == "WARTS":
        collection = "NETHER_STALK"
    elif crop == "CANE":
        collection = "SUGAR_CANE"

    ff = 0
    # hoe rarity
    hoe = inv.get("attributes", {}).get("id")
    if hoe == f"THEORETICAL_HOE_{crop}_1":
        ff += 10
    elif hoe == f"THEORETICAL_HOE_{crop}_2":
        ff += 25
    elif hoe == f"THEORETICAL_HOE_{crop}_3":
        ff += 50
    # turbo warts
    ff += (
        inv.get("attributes", {})
        .get("enchantments", {})
        .get(f"turbo_{crop.lower()}", 0)
    ) * 5
    # ffd
    ff += inv.get("stats", {}).get("farming_fortune", 0)

    # wart collection analysis
    if hoe == f"THEORETICAL_HOE_{crop}_3":
        collection = (
            int(log10(r["members"][mcuuid]["collection"].get(collection, 1)) + 1) - 4
        )
        ff += collection * 8
    # wart logarithmic counter
    if hoe in [f"THEORETICAL_HOE_{crop}_2", f"THEORETICAL_HOE_{crop}_3"]:
        try:
            for line in inv.get("lore"):
                if "Counter: " in line:
                    counter = line
        except TypeError:
            counter = 0
        counter = sub("§[0-9a-fk-or]", "", counter)
        counter = int(sub("[^-0-9\/]+", "", counter))

        counter = int(log10(counter) + 1) - 4
        ff += counter * 16

        return ff


def rates(ctx, mcuuid, profile):
    if profile is None:
        request = requests.get(
            f"https://api.slothpixel.me/api/skyblock/profile/{mcuuid}?key={key}"
        )
    else:
        request = requests.get(
            f"https://api.slothpixel.me/api/skyblock/profile/{mcuuid}/{profile}?key={key}"
        )
    r = request.json()

    if r.get("error") == "Profile not found!":
        embed = Embed(description="Invalid profile!", colour=ctx.guild.me.color)
        embed.set_footer(**footer_text)
        return embed
    elif (
        r.get("error")
        == "undefined is not iterable (cannot read property Symbol(Symbol.iterator))"
    ):
        embed = Embed(
            description="um i dont think this guy has played skyblock",
            colour=ctx.guild.me.color,
        )
        embed.set_footer(**footer_text)
        return embed

    # general ff
    # fortune from farming level
    total_xp = r["members"][mcuuid]["skills"].get("farming", {}).get("xp", 0)
    perks = r["members"][mcuuid]["jacob2"]["perks"]

    farming_level = lvcheck(total_xp, (perks.get("farming_level_cap", 0) + 50))

    # fortune from anita bonus
    anita = perks.get("double_drops", 0)

    # fortune from elephant

    pets = r["members"][mcuuid]["active_pet"]
    pet_name = pets.get("name", "")
    pet_rarity = pets.get("rarity", "")

    if pet_name == "Elephant" and pet_rarity == "LEGENDARY":
        pet_level = r["members"][mcuuid]["active_pet"]["level"]
    else:
        pet_level = 0

    # fortune from general hoe
    gen_hoe = 0

    try:
        inv = r["members"][mcuuid]["inventory"][0]
    except IndexError:
        inv = {}

    # hoe reforge
    reforge = inv.get("attributes", {}).get("modifier")
    rarity = inv.get("rarity")

    if reforge == "blessed":
        if rarity == "mythic":
            gen_hoe += 20
        elif rarity == "legendary":
            gen_hoe += 16
        elif rarity == "epic":
            gen_hoe += 13
        elif rarity == "rare":
            gen_hoe += 9
        elif rarity == "uncommon":
            gen_hoe += 7
        elif rarity == "common":
            gen_hoe += 5
    # harvesting
    harvesting = inv.get("attributes", {}).get("enchantments", {}).get("harvesting", 0)
    gen_hoe += harvesting * 12.5
    # cultivating
    gen_hoe += inv.get("attributes", {}).get("enchantments", {}).get("cultivating", 0)
    # farming for dummies

    ff = (farming_level * 4) + (anita * 2) + (pet_level * 1.8) + gen_hoe

    try:
        wart_ff = ff + crops(r, mcuuid, inv, "WARTS")
        wart_coins = 3 * (2 * (1 + wart_ff / 100))
        wart_coins_per_hour = "{:,.1f}".format(wart_coins * 72000)
    except TypeError:
        wart_ff = "N/A"
        wart_coins_per_hour = "NaN"

    try:
        cane_ff = ff + crops(r, mcuuid, inv, "CANE")
        cane_coins = 3 * (2 * (1 + cane_ff / 100))
        cane_coins_per_hour = "{:,.1f}".format(cane_coins * 144000)
    except TypeError:
        cane_ff = "N/A"
        cane_coins_per_hour = "NaN"

    ign = r["members"][mcuuid]["player"]["username"]
    fruit = r["cute_name"]

    embed = Embed(
        title=f"Rates for {ign} ({fruit})",
        colour=ctx.guild.me.color,
    )
    embed.add_field(
        name="<:Warts:862984331677138955> Warts (NPC)",
        value=f"{wart_coins_per_hour}/hour\n{wart_ff} ff",
    )
    embed.add_field(
        name="<:cane:877082351417585675> Cane (BZ)",
        value=f"{cane_coins_per_hour}/hour\n{cane_ff} ff",
    )
    embed.set_footer(
        text="Made by yan#0069 • Inaccurate? Make sure your hoe is in your first slot",
        icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
    )
    return embed


def manualrates(ctx, ff):
    wart_coins = 3 * (2 * (1 + ff / 100))
    wart_coins_per_hour = "{:,.1f}".format(wart_coins * 72000)
    ff = "{:,}".format(ff)
    embed = Embed(
        title=f"Rates for {ff} farming fortune",
        colour=ctx.guild.me.color,
    )
    embed.add_field(
        name="<:Warts:862984331677138955> Warts (NPC)",
        value=f"{wart_coins_per_hour}/hour",
    )
    embed.set_footer(**footer_text)
    return embed
