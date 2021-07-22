import requests
from discord import Embed, Colour
from discord.ext import commands
from math import log10
from re import sub
from util.config import key
from util.skill import lvcheck
from util.uuid import uuid


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["r"])
    async def rates(self, ctx, ign, profile=None):
        embed = Embed(
            description="If this message doesn't update within a few seconds, make sure all your API is on and your hoe is in your first hotbar slot.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="loading aaaa", value="_ _", inline=False)
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )
        msg = await ctx.send(embed=embed)
        mcuuid = uuid(ign)
        if profile is None:
            request = requests.get(
                f"https://api.slothpixel.me/api/skyblock/profile/{mcuuid}?key={key}"
            )
        else:
            request = requests.get(
                f"https://api.slothpixel.me/api/skyblock/profile/{mcuuid}/{profile}?key={key}"
            )
        r = request.json()

        # general ff
        # fortune from farming level
        total_xp = r["members"][mcuuid]["skills"]["farming"]["xp"]
        try:
            cap = r["members"][mcuuid]["jacob2"]["perks"]["farming_level_cap"] + 50
        except KeyError:
            cap = 50

        farming_level = lvcheck(total_xp, cap)

        # fortune from anita bonus
        try:
            anita = r["members"][mcuuid]["jacob2"]["perks"]["double_drops"]
        except KeyError:
            anita = 0

        # fortune from elephant
        try:
            pet_name = r["members"][mcuuid]["active_pet"]["name"]
            pet_rarity = r["members"][mcuuid]["active_pet"]["rarity"]
        except KeyError:
            pet_name = ""
            pet_rarity = ""

        if pet_name == "Elephant" and pet_rarity == "LEGENDARY":
            pet_level = r["members"][mcuuid]["active_pet"]["level"]
        else:
            pet_level = 0

        # fortune from general hoe
        gen_hoe = 0

        try:
            hoe = r["members"][mcuuid]["inventory"][0]["attributes"]["id"]
        except KeyError:
            embed = Embed(
                title="Error",
                description="You must place your hoe in your first hotbar slot!",
                colour=Colour.red,
            )
            embed.set_footer(
                text="sorry im bad at this ok",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )
            await msg.edit(embed=embed)

            embed.set_footer(
                text="sorry im bad at this ok",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )
            await msg.edit(embed=embed)

        # hoe reforge
        try:
            reforge = r["members"][mcuuid]["inventory"][0]["attributes"]["modifier"]
        except KeyError:
            reforge = ""
        try:
            rarity = r["members"][mcuuid]["inventory"][0]["rarity"]
        except KeyError:
            rarity = ""

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
        try:
            harvesting = r["members"][mcuuid]["inventory"][0]["attributes"][
                "enchantments"
            ]["harvesting"]
        except KeyError:
            harvesting = 0
        for i in range(harvesting):
            gen_hoe += 12.5
        # cultivating
        try:
            cultivating = r["members"][mcuuid]["inventory"][0]["attributes"][
                "enchantments"
            ]["cultivating"]
        except KeyError:
            cultivating = 0
        for i in range(cultivating):
            gen_hoe += 1
        # farming for dummies
        ffd = 0
        for i in range(36):
            try:
                ffd += r["members"][mcuuid]["inventory"][i]["stats"]["farming_fortune"]
            except KeyError:
                ffd += 0

        # wart hoe fortune
        wart_hoe = 0
        # hoe rarity
        if hoe == "THEORETICAL_HOE_WARTS_1":
            wart_hoe += 10
        elif hoe == "THEORETICAL_HOE_WARTS_2":
            wart_hoe += 25
        elif hoe == "THEORETICAL_HOE_WARTS_3":
            wart_hoe += 50
        # turbo warts
        try:
            turbo_warts = r["members"][mcuuid]["inventory"][0]["attributes"][
                "enchantments"
            ]["turbo_warts"]
        except KeyError:
            turbo_warts = 0
        for i in range(turbo_warts):
            wart_hoe += 5
        # wart collection analysis
        if hoe == "THEORETICAL_HOE_WARTS_3":
            try:
                wart_collection = r["members"][mcuuid]["collection"]["NETHER_STALK"]
            except KeyError:
                wart_collection = 1

            wart_collection = int(log10(wart_collection) + 1) - 4
            wart_hoe += wart_collection * 8
        # wart logarithmic counter
        if hoe in ["THEORETICAL_HOE_WARTS_2", "THEORETICAL_HOE_WARTS_3"]:
            try:
                for line in r["members"][mcuuid]["inventory"][0]["lore"]:
                    if "Counter: " in line:
                        counter = line
            except KeyError:
                counter = 0
            counter = sub("§[0-9a-fk-or]", "", counter)
            counter = int(sub("[^-0-9\/]+", "", counter))

            counter = int(log10(counter) + 1) - 4
            wart_hoe += counter * 16

        ff = (farming_level * 4) + (anita * 2) + (pet_level * 1.8) + gen_hoe + ffd
        wart_ff = ff + wart_hoe

        wart_coins = 3 * (2 * (1 + wart_ff / 100))
        wart_coins_per_hour = "{:,.1f}".format(wart_coins * 20 * 60 * 60)

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
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )
        await msg.edit(embed=embed)

    @commands.command(aliases=["mr", "manrates"])
    async def manualrates(self, ctx, ff):
        wart_coins = 3 * (2 * (1 + int(ff) / 100))
        wart_coins_per_hour = "{:,.1f}".format(wart_coins * 20 * 60 * 60)

        embed = Embed(
            title=f"Rates for {ff} farming fortune",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="<:Warts:862984331677138955> Warts (NPC)",
            value=f"{wart_coins_per_hour}/hour",
        )
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Farming(bot))
