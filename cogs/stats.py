import requests
from discord import Embed
from discord.ext import commands
from util.config import key
from util.uuid import uuid


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["s"])
    async def stats(self, ctx, ign, profile=None):
        embed = Embed(
            description="If this message doesn't update within a few seconds, sorry :cry:",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="HYPIXEL WHY are you so sLOW", value="_ _", inline=False)
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )
        msg = await ctx.send(embed=embed)
        mcuuid = uuid(ign)
        if profile is None:
            request = requests.get(
                f"https://hypixel-api.senither.com/v1/profiles/{mcuuid}/latest?key={key}"
            )
        else:
            request = requests.get(
                f"https://hypixel-api.senither.com/v1/profiles/{mcuuid}/{profile}?key={key}"
            )
        r = request.json()

        ign = r["data"]["username"]
        fruit = r["data"]["name"]

        print(f"fetched {ign}'s data: {request}")

        if r["data"]["skills"]["apiEnabled"] is True:
            asl = round(r["data"]["skills"]["average_skills"], 2)
        elif r["data"]["skills"]["apiEnabled"] is False:
            asl = "API off"
        else:
            asl = "?"
        try:
            weight = "{:,}".format(int(r["data"]["weight"]))
            overflow = "{:,}".format(int(r["data"]["weight_overflow"]))
        except KeyError:
            weight = "?"
            overflow = "?"
        try:
            zombie = int(r["data"]["slayers"]["bosses"]["revenant"]["level"])
        except KeyError:
            zombie = "?"
        try:
            spider = int(r["data"]["slayers"]["bosses"]["tarantula"]["level"])
        except KeyError:
            spider = "?"
        try:
            wolf = int(r["data"]["slayers"]["bosses"]["sven"]["level"])
        except KeyError:
            wolf = "?"
        try:
            enderman = int(r["data"]["slayers"]["bosses"]["enderman"]["level"])
        except KeyError:
            enderman = "?"
        try:
            coins = "{:,}".format(int(r["data"]["coins"]["total"]))
        except KeyError:
            coins = "?"
        try:
            cata = int(r["data"]["dungeons"]["types"]["catacombs"]["level"])
            secrets = "{:,}".format(r["data"]["dungeons"]["secrets_found"])
        except TypeError:
            cata = "?"
            secrets = "?"

        print(asl, weight, zombie, spider, wolf, enderman, coins, cata, secrets)

        embed = Embed(title=f"Stats for {ign} ({fruit})", colour=ctx.guild.me.color)
        embed.set_thumbnail(
            url=f"https://crafatar.com/renders/body/{mcuuid}?overlay=true"
        )
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
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await msg.edit(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Stats(bot))