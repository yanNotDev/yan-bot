import json

from discord import Embed
from util.config import lbin_footer_text


def fragrun(ctx, runs, time):
    if runs == 1:
        embed = Embed(title="Average loot from one fragrun", colour=ctx.guild.me.color)
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

    embed.add_field(name="Diamante's Handle", value=f"x{runs} ({handle_profit} coins)")
    embed.add_field(name="Jolly Pink Rock", value=f"x{runs} ({rock_profit} coins)")
    embed.add_field(name="L.A.S.R.'s Eye", value=f"x{runs} ({lasr_profit} coins)")
    embed.add_field(name="Bigfoot's Lasso", value=f"x{runs} ({lasso_profit} coins)")
    embed.add_field(name="Total", value=f"{total_profit} coins")

    embed.set_footer(**lbin_footer_text)

    return embed
