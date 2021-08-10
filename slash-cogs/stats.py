import requests
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from util.config import footer_text, key
from util.uuid import uuid


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description="Shows a player's general skyblock stats.",
        # guild_ids=guilds,
        options=[
            create_option("ign", "IGN", 3, False),
            create_option("profile", "Profile", 3, False),
        ],
    )
    async def stats(self, ctx, ign=None, profile=None):
        mcuuid = await uuid(self.bot, ctx.author.id, ign)
        if mcuuid == 204:
            await ctx.send("Invalid IGN!", hidden=True)
            return
        elif mcuuid == KeyError:
            await ctx.send(
                f"Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                hidden=True,
            )
            return

        embed = Embed(
            description="If this message doesn't update within a few seconds, sorry :cry:",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="HYPIXEL WHY are you so sLOW", value="_ _", inline=False)
        embed.set_footer(**footer_text)
        msg = await ctx.send(embed=embed)

        if profile is None:
            request = requests.get(
                f"https://hypixel-api.senither.com/v1/profiles/{mcuuid}/latest?key={key}"
            )
        else:
            request = requests.get(
                f"https://hypixel-api.senither.com/v1/profiles/{mcuuid}/{profile}?key={key}"
            )
        r = request.json()

        try:
            if r["reason"] == "Failed to find a profile using the given strategy":
                embed = Embed(description="Invalid profile!", colour=ctx.guild.me.color)
                embed.set_footer(**footer_text)
                await msg.edit(embed=embed)
                return

            elif r["reason"].startswith(
                "Found no SkyBlock profiles for a user with a UUID of '"
            ):
                embed = Embed(
                    description="um i dont think this guy has played skyblock",
                    colour=ctx.guild.me.color,
                )
                embed.set_footer(**footer_text)
                await msg.edit(embed=embed)
                return

        except KeyError:
            pass

        ign = r["data"]["username"]
        fruit = r["data"]["name"]

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
        embed.set_footer(**footer_text)

        await msg.edit(embed=embed)

    @cog_ext.cog_slash(
        description="Get's the UUID of someone's Minecraft IGN.",
        # guild_ids=guilds,
        options=[
            create_option("ign", "IGN", 3, False),
        ],
    )
    async def mcuuid(self, ctx, ign=None):
        id = await uuid(self.bot, ctx.author.id, ign)
        if id == 204:
            await ctx.send("Invalid IGN!", hidden=True)
        elif id == KeyError:
            await ctx.send(
                f"Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                hidden=True,
            )
        else:
            if ign is None:
                msg = f"You have the UUID `{id}`"
            else:
                msg = f"{ign} has the UUID `{id}`"
            await ctx.send(msg)


def setup(bot: commands.Bot):
    bot.add_cog(Stats(bot))
