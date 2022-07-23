from util.blacklist import slash_blacklist
from commands import bits, calc, fragrun
from discord.ext import commands
from discord import app_commands
from typing import Literal


class SlashCalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        description="Checks xp required to get from one Catacombs level to another.",
    )
    @app_commands.describe(start="Staring level", end="Ending level", xp="XP per floor")
    async def calccata(self, interaction, start: int, end: int, xp: float | None):
        embed = calc.calccata(interaction, start, end, xp)
        if embed == IndexError:
            await interaction.response.send_message(
                "You can't enter a level higher than 50!", ephemeral=True
            )
        else:
            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(
        description="Checks xp required to get from one level to another, for the 7 main skills.",
    )
    @app_commands.describe(start="Staring level", end="Ending level")
    async def calcskill(self, interaction, start: int, end: int):
        embed = calc.calcskill(interaction, start, end)
        if embed == IndexError:
            await interaction.response.send_message(
                "You can't enter a level higher than 60!", ephemeral=True
            )
        else:
            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(
        description="Checks xp required to get from one slayer level to another.",
    )
    @app_commands.describe(
        start="Starting level",
        end="Ending level",
        type="Type",
        aatrox="Is Aatrox active",
    )
    async def calcslayer(
        self,
        interaction,
        start: int,
        end: int,
        type: Literal["Revenant", "Tarantula", "Other"],
        aatrox: bool | None,
    ):
        aatrox = aatrox or False
        embed = calc.calcslayer(interaction, start, end, type, aatrox)
        if embed == IndexError:
            await interaction.response.send_message(
                "Slayer level can only be from 0 to 9!", ephemeral=True
            )
        else:
            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(
        description="Calculates average profit from fragrunning.",
    )
    @app_commands.describe(
        runs="Number of fragruns", time="Time in minutes to finish 1 fragrun"
    )
    async def fragrun(self, interaction, runs: int, time: float | None):
        embed = fragrun.fragrun(interaction, runs, time)
        ephemeral = await slash_blacklist(self.bot, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(
        description="Calculates coins per bit for all auctionable items.",
    )
    async def bits(self, interaction):
        embed = bits.bits(interaction)

        ephemeral = await slash_blacklist(self.bot, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(
        description="Calculates the amount of powder needed from a start level to an end level.",
    )
    @app_commands.describe(
        perk="HOTM Perk", startlevel="Starting level", endinglevel="Ending level"
    )
    async def calcpowder(
        self,
        interaction,
        perk: Literal[
            "Mining Speed",
            "Mining Fortune",
            "Quick Forge",
            "Titanium Insanium",
            "Daily Powder",
            "Luck of The Cave",
            "Crystallized",
            "Effecient Miner",
            "Orbiter",
            "Seasoned Mineman",
            "Mole",
            "Professional",
            "Lonesome Miner",
            "Great Explorer",
            "Fortunate",
            "Powder Buff",
            "Mining Speed Two",
            "Mining Fortune Two",
        ],
        startlevel: int,
        endinglevel: int,
    ):
        embed = calc.calcpowder(interaction, perk, startlevel, endinglevel)

        if isinstance(embed, str):
            await interaction.response.send_message(embed, ephemeral=True)

        ephemeral = await slash_blacklist(self.bot, interaction)

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCalc(bot))
