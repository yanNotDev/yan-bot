from math import log10
from re import sub

import requests
from discord import Embed
from util.config import footer_text, key


def lvcheck(xp, cap):
    table = [ 50, 125, 200, 300, 500, 750, 1000, 1500, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1500000, 1600000, 1700000, 1800000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2750000, 2900000, 3100000, 3400000, 3700000, 4000000, 4300000, 4600000, 4900000, 5200000, 5500000, 5800000, 6100000, 6400000, 6700000, 7000000, ]
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
    total_xp = r["members"][mcuuid]["skills"]["farming"]["xp"]
    perks = r["members"][mcuuid]["jacob2"]["perks"]
    cap = perks.get("farming_level_cap", 0) + 50
    farming_level = lvcheck(total_xp, cap)

    # fortune from anita bonus
    anita = perks.get("double_drops", 0)

    # fortune from elephant

    pets = r["members"][mcuuid]["active_pet"]
    pet_name = r.get("name", "")
    pet_rarity = r.get("rarity", "")

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
    reforge = inv.get("attributes", {}).get("modifier", "")
    rarity = inv.get("rarity", "")

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
    for i in range(harvesting):
        gen_hoe += 12.5
    # cultivating
    cultivating = (
        inv.get("attributes", {}).get("enchantments", {}).get("cultivating", 0)
    )
    for i in range(cultivating):
        gen_hoe += 1
    # farming for dummies
    ffd = 0
    for i in range(36):
        try:
            ffd += (
                r["members"][mcuuid]["inventory"][i]
                .get("stats", {})
                .get("farming_fortune", 0)
            )
        except IndexError:
            pass

    # wart hoe fortune
    wart_hoe = 0
    # hoe rarity
    hoe = inv.get("attributes", {}).get("id")
    if hoe == "THEORETICAL_HOE_WARTS_1":
        wart_hoe += 10
    elif hoe == "THEORETICAL_HOE_WARTS_2":
        wart_hoe += 25
    elif hoe == "THEORETICAL_HOE_WARTS_3":
        wart_hoe += 50
    # turbo warts
    turbo_warts = (
        inv.get("attributes", {}).get("enchantments", {}).get("turbo_warts", 0)
    )
    for i in range(turbo_warts):
        wart_hoe += 5
    # wart collection analysis
    if hoe == "THEORETICAL_HOE_WARTS_3":
        wart_collection = r["members"][mcuuid]["collection"].get("NETHER_STALK", 1)

        wart_collection = int(log10(wart_collection) + 1) - 4
        wart_hoe += wart_collection * 8
    # wart logarithmic counter
    if hoe in ["THEORETICAL_HOE_WARTS_2", "THEORETICAL_HOE_WARTS_3"]:
        try:
            for line in inv.get("lore"):
                if "Counter: " in line:
                    counter = line
        except TypeError:
            counter = 0
        counter = sub("§[0-9a-fk-or]", "", counter)
        counter = int(sub("[^-0-9\/]+", "", counter))

        counter = int(log10(counter) + 1) - 4
        wart_hoe += counter * 16

    ff = (farming_level * 4) + (anita * 2) + (pet_level * 1.8) + gen_hoe + ffd
    wart_ff = ff + wart_hoe

    wart_coins = 3 * (2 * (1 + wart_ff / 100))
    wart_coins_per_hour = "{:,.1f}".format(wart_coins * 72000)

    ign = r["members"][mcuuid]["player"]["username"]
    fruit = r["cute_name"]

    embed = Embed(
        title=f"Rates for {ign} ({fruit})",
        description=f"{wart_ff} total farming fortune",
        colour=ctx.guild.me.color,
    )
    embed.add_field(
        name="<:Warts:862984331677138955> Warts (NPC)",
        value=f"{wart_coins_per_hour}/hour",
        inline=True,
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
