import requests
from discord import Embed
from util.config import key, footer_text


def stats(ctx, mcuuid, profile):
    if profile is None:
        request = requests.get(
            f"https://hypixel-api.senither.com/v1/profiles/{mcuuid}/latest?key={key}"
        )
    else:
        request = requests.get(
            f"https://hypixel-api.senither.com/v1/profiles/{mcuuid}/{profile}?key={key}"
        )
    r = request.json()

    if r.get("reason") == "Failed to find a profile using the given strategy":
        embed = Embed(description="Invalid profile!", colour=ctx.guild.me.color)
        embed.set_footer(**footer_text)
        return embed

    elif r.get("reason", "a string").startswith(
        "Found no SkyBlock profiles for a user with a UUID of '"
    ):
        embed = Embed(
            description="um i dont think this guy has played skyblock",
            colour=ctx.guild.me.color,
        )
        embed.set_footer(**footer_text)
        return embed


    ign = r["data"]["username"]
    fruit = r["data"]["name"]

    apiEnabled = r["data"]["skills"]["apiEnabled"]

    if apiEnabled: 
        asl = round(r["data"]["skills"]["average_skills"], 2)
    elif not apiEnabled: 
        asl = "API off"
    else:
        asl = "?"

    weight = "{:,}".format(round(r["data"]["weight"]))
    overflow = "{:,}".format(round(r["data"]["weight_overflow"]))

    zombie = int(r["data"]["slayers"]["bosses"]["revenant"]["level"])
    spider = int(r["data"]["slayers"]["bosses"]["tarantula"]["level"])
    wolf = int(r["data"]["slayers"]["bosses"]["sven"]["level"])
    enderman = int(r["data"]["slayers"]["bosses"]["enderman"]["level"])

    coins = "{:,}".format(int(r["data"]["coins"]["total"]))

    try:
        cata = int(r["data"]["dungeons"]["types"]["catacombs"]["level"])
        secrets = "{:,}".format(r["data"]["dungeons"]["secrets_found"])
    except TypeError:
        cata = "?"
        secrets = "?"

    embed = Embed(title=f"Stats for {ign} ({fruit})", colour=ctx.guild.me.color)
    embed.set_thumbnail(url=f"https://crafatar.com/renders/body/{mcuuid}?overlay=true")
    embed.add_field(name="Skill Average", value=asl, inline=True)
    embed.add_field(name="Cata Level", value=cata, inline=True)
    embed.add_field(name="Secrets", value=secrets, inline=True)
    embed.add_field(
        name="Weight + Overflow", value=f"{weight} + {overflow}", inline=True
    )
    embed.add_field(name="Coins", value=coins, inline=True)
    embed.add_field(
        name="Slayers", value=f"{zombie}/{spider}/{wolf}/{enderman}", inline=True
    )
    embed.set_footer(**footer_text)

    return embed
