from util.blacklist import slash_blacklist
from commands import rates
from commands.uuid import uuid
from discord import Embed, app_commands
from discord.ext import commands
from util.config import footer_text


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        description="Calculate coins per hour from farming.",
    )
    @app_commands.describe(ign="IGN", profile="Profile")
    async def rates(self, interaction, ign: str | None, profile: str | None):
        mcuuid = await uuid(self.bot, interaction.user.id, ign)
        if mcuuid == 204:
            await interaction.response.send_message("Invalid IGN!")
            return
        elif mcuuid == KeyError:
            await interaction.response.send_message(
                "Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
            )
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, make sure all your API is on and your hoe is in your first hotbar slot.",
                colour=interaction.guild.me.color,
            )
            embed.add_field(name="loading aaaa", value="_ _", inline=False)
            embed.set_footer(**footer_text)
            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

            embed = rates.rates(interaction, mcuuid, profile)
            await interaction.edit_original_message(embed=embed)

    @app_commands.command(
        description="Calculate coins per hour from farming.",
    )
    @app_commands.describe(ff="Farming Fortune")
    async def manualrates(self, interaction, ff: int):
        ephemeral = await slash_blacklist(self.bot, interaction)

        embed = rates.manualrates(interaction, ff)

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


async def setup(bot):
    await bot.add_cog(Farming(bot))
