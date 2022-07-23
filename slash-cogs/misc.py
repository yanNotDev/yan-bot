from typing import Literal

from commands import misc
from discord import app_commands
from discord.ext import commands
from util.blacklist import slash_blacklist


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @app_commands.command(description="Displays the help message.")
    @app_commands.describe(command="Command name")
    async def help(
        self,
        interaction,
        command: Literal[
            "Rates",
            "Manaul Rates",
            "Stats",
            "Calc Skill",
            "Calc Cata",
            "Calc Slayer",
            "Fragrun",
            "Bits",
            "GEXP",
            "MCuuid",
            "Link",
            "Prefix",
            "Blacklist",
            "Ban channel",
            "VCrole",
            "Help",
            "Info",
        ]
        | None,
    ):
        ephemeral = await slash_blacklist(self.bot, interaction)
        embed = misc.help(interaction, command)
        await interaction.response.send_message(**embed, ephemeral=ephemeral)

    @app_commands.command(
        description="Displays general info about the bot.",
    )
    async def info(self, interaction):
        embed = misc.info(self.bot, interaction)
        ephemeral = await slash_blacklist(self.bot, interaction)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))
