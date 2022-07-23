from math import ceil

from discord import Embed
from util.config import footer_text


def catadiff(start, end):
    table = [
        0,
        50,
        125,
        235,
        395,
        625,
        955,
        1425,
        2095,
        3045,
        4385,
        6275,
        8940,
        12700,
        17960,
        25340,
        35640,
        50040,
        70040,
        97640,
        135640,
        188140,
        259640,
        356640,
        488640,
        668640,
        911640,
        1239640,
        1684640,
        2284640,
        3084640,
        4149640,
        5559640,
        7459640,
        9959640,
        13259640,
        17559640,
        23159640,
        30359640,
        39559640,
        51559640,
        66559640,
        85559640,
        109559640,
        139559640,
        177559640,
        225559640,
        285559640,
        360559640,
        453559640,
        569809640,
    ]
    begin = table[int(start)]
    finish = table[int(end)]
    return finish - begin


def calccata(ctx, start, end, xp):
    try:
        required_int = catadiff(start, end)
    except IndexError:
        return IndexError

    required = "{:,}".format(required_int)

    embed = Embed(
        description=f"{required} xp is required to get from Catacombs {start} to {end}.",
        colour=ctx.guild.me.color,
    )
    if xp is not None:
        runs = "{:,}".format(ceil(required_int / xp))
        embed.add_field(name=f"Runs required to reach Catacombs {end}", value=runs)
    embed.set_footer(**footer_text)
    return embed


def lvdiff(start, end):
    table = [
        0,
        50,
        175,
        375,
        675,
        1175,
        1925,
        2925,
        4425,
        6425,
        9925,
        14925,
        22425,
        32425,
        47425,
        67425,
        97425,
        147425,
        222425,
        322425,
        522425,
        822425,
        1222425,
        1722425,
        2322425,
        3022425,
        3822425,
        4722425,
        5722425,
        6822425,
        8022425,
        9322425,
        10722425,
        12222425,
        13822425,
        15522425,
        17322425,
        19222425,
        21222425,
        23322425,
        25522425,
        27822425,
        30222425,
        32722425,
        35322425,
        38072425,
        40972425,
        44072425,
        47472425,
        51172425,
        55172425,
        59472425,
        64072425,
        68972425,
        74172425,
        79672425,
        85472425,
        91572425,
        97972425,
        104672425,
        111672425,
    ]
    begin = table[int(start)]
    finish = table[int(end)]
    return finish - begin


def calcskill(ctx, start, end):
    try:
        required = "{:,}".format(lvdiff(start, end))
    except IndexError:
        return IndexError

    embed = Embed(
        description=f"{required} xp is required to get from Level {start} to {end}.",
        colour=ctx.guild.me.color,
    )
    embed.set_footer(**footer_text)

    return embed


def slayerdiff(start, end, slayer):
    table = []
    if slayer == "Revenant":
        table = [0, 5, 15, 200, 1000]
    elif slayer == "Tarantula":
        table = [0, 5, 25, 200, 1000]
    elif slayer == "Other":
        table = [0, 10, 30, 250, 1500]
    table.extend([5000, 20000, 100000, 400000, 1000000])
    begin = table[int(start)]
    finish = table[int(end)]
    return finish - begin


def calcslayer(ctx, start, end, type, aatrox):
    try:
        required = slayerdiff(start, end, type)
    except IndexError:
        return IndexError

    required_str = "{:,}".format(required)

    if not aatrox:
        t1_xp, t1_cost = 5, 2000
        t2_xp, t2_cost = 25, 7500
        t3_xp, t3_cost = 100, 20000
        t4_xp, t4_cost = 500, 50000
        t5_xp, t5_cost = 1500, 100000
    else:
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
        embed.add_field(name="T5", value=f"{t5} ({t5_total_cost} coins)", inline=False)
    embed.set_footer(**footer_text)

    return embed


def miningSpeed(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def miningFortune(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.05
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def quickForge(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 4
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def titaniumInsanium(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.1
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def dailyPowder(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + 200 + ((start - 1) * 18)
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def luckofTheCave(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.07
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def crystallized(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.4
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def effecientMiner(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 2.6
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def orbiter(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + start * 70
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def seasonedMineman(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 2.3
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def mole(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 2.2
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def professional(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 2.3
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def LonesomeMiner(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.07
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def greatExplorer(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 4
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def fortunate(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.05
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def powderBuff(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.2
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def miningSpeedtwo(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.2
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def miningFortunetwo(start, end):
    totalPowder = 0
    start += 1
    for i in range(start, end + 1):
        totalPowder = totalPowder + (start + 1) ** 3.2
        start = start + 1
    return "{:,.0f}".format(totalPowder)


def calcpowder(ctx, perk, startlevel, endinglevel):
    powder = 0
    if startlevel == endinglevel:
        return "You can't start from the same level as you end at."
    else:
        perk = perk.lower()
        if perk == "mining speed":
            if startlevel and endinglevel <= 50:
                powder = miningSpeed(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 50."
        elif perk == "mining fortune":
            if startlevel and endinglevel <= 50:
                powder = miningFortune(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 50"
        elif perk == "quick forge":
            if startlevel and endinglevel <= 20:
                powder = quickForge(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 20"
        elif perk == "titamium insanium":
            if startlevel and endinglevel <= 50:
                powder = titaniumInsanium(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 50"
        elif perk == "daily powder":
            if startlevel and endinglevel <= 100:
                powder = dailyPowder(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 100"
        elif perk == "luck of the cave":
            if startlevel and endinglevel <= 45:
                powder = luckofTheCave(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 45"
        elif perk == "crystallized":
            if startlevel and endinglevel <= 30:
                powder = crystallized(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 30"
        elif perk == "effecient miner":
            if startlevel and endinglevel <= 100:
                powder = effecientMiner(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 100"
        elif perk == "orbiter":
            if startlevel and endinglevel <= 80:
                powder = orbiter(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 80"
        elif perk == "seasoned mineman":
            if startlevel and endinglevel <= 100:
                powder = seasonedMineman(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 100"
        elif perk == "mole":
            if startlevel and endinglevel <= 190:
                powder = mole(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 190"
        elif perk == "professional":
            if startlevel and endinglevel <= 140:
                powder = professional(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 140"
        elif perk == "lonesome miner":
            if startlevel and endinglevel <= 45:
                powder = LonesomeMiner(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 45"
        elif perk == "great explorer":
            if startlevel and endinglevel <= 20:
                powder = greatExplorer(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 20"
        elif perk == "fortunate":
            if startlevel and endinglevel <= 20:
                powder = fortunate(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 20"
        elif perk == "powder buff":
            if startlevel and endinglevel <= 50:
                powder = powderBuff(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 50"
        elif perk == "mining speed two":
            if startlevel and endinglevel <= 50:
                powder = miningSpeedtwo(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 50"
        elif perk == "mining fortune two":
            if startlevel and endinglevel <= 50:
                powder = miningFortunetwo(startlevel, endinglevel)
            else:
                return "The maximum level for this perk is 50"
        embed = Embed(
            description=f"{powder} powder required from level {startlevel} to level {endinglevel}.",
            colour=ctx.guild.me.color,
        )
        embed.set_footer(**footer_text)

        return embed
