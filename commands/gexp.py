from datetime import datetime
import requests
from discord import Embed
from pytz import timezone
from util.config import footer_text, key


def gexp(ctx, ign, mcuuid):
    r = requests.get(f"https://api.hypixel.net/guild?key={key};player={mcuuid}").json()

    embed = Embed(color=ctx.guild.me.colour)
    embed.set_footer(**footer_text)

    if r["guild"] is None:
        embed.add_field(name="This person is not in any guild!", value="_ _")
        return embed

    embed.set_thumbnail(url=f"https://crafatar.com/renders/body/{mcuuid}?overlay=true")

    for member in r["guild"]["members"]:
        if mcuuid == member["uuid"]:
            date = datetime.now(timezone("EST"))
            gexp = member["expHistory"][f"{date.year}-{date.month}-{date.day}"]
            if ign is None:
                embed.add_field(
                    name=f"You have {gexp} Guild EXP.", value="_ _", inline=False
                )
            else:
                embed.add_field(
                    name=f"{ign} has {gexp} Guild EXP.", value="_ _", inline=False
                )
            return embed
