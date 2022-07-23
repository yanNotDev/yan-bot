from util.blacklist import slash_blacklist
from commands import gexp, stats
from commands.uuid import uuid
from discord import Embed
from discord.ext import commands
from discord import app_commands
from util.config import footer_text


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        description="Shows a player's general skyblock stats.",
    )
    @app_commands.describe(ign="IGN", profile="Profile")
    async def stats(self, interaction, ign: str | None, profile: str | None):
        mcuuid = await uuid(self.bot, interaction.user.id, ign)
        if mcuuid == 204:
            await interaction.response.send_message("Invalid IGN!", ephemeral=True)
        elif mcuuid == KeyError:
            await interaction.response.send_message(
                f"Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                ephemeral=True,
            )
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, sorry :cry:",
                colour=interaction.guild.me.color,
            )
            embed.add_field(name="HYPIXEL WHY are you so sLOW", value="_ _", inline=False)
            embed.set_footer(**footer_text)

            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

            embed = stats.stats(interaction, mcuuid, profile)

            await interaction.edit_original_message(embed=embed)

    @app_commands.command(
        description="Get's the UUID of someone's Minecraft IGN.",
    )
    @app_commands.describe(ign="IGN")
    async def mcuuid(self, interaction, ign: str | None):
        id = await uuid(self.bot, interaction.user.id, ign)
        if id == 204:
            await interaction.response.send_message("Invalid IGN!", ephemeral=True)
        elif id == KeyError:
            await interaction.response.send_message(
                f"Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                ephemeral=True,
            )
        else:
            if ign is None:
                msg = f"You have the UUID `{id}`"
            else:
                msg = f"{ign} has the UUID `{id}`"

            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(msg, ephemeral=ephemeral)

    @app_commands.command(
        description="Gets the Guild XP for the past 7 days.",
    )
    @app_commands.describe(ign="IGN")
    async def gexp(self, interaction, ign: str | None):
        mcuuid = await uuid(self.bot, interaction.user.id, ign)
        if mcuuid == 204:
            await interaction.response.send_message("Invalid IGN!", ephemeral=True)
        elif mcuuid == KeyError:
            await interaction.response.send_message(
                f"Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                ephemeral=True,
            )
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, sorry :cry:",
                colour=interaction.guild.me.color,
            )
            embed.add_field(name="HYPIXEL WHY are you so sLOW", value="_ _", inline=False)
            embed.set_footer(**footer_text)

            ephemeral = await slash_blacklist(self.bot, interaction)
            msg = await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

            embed = gexp.gexp(interaction, ign, mcuuid)

            await interaction.edit_original_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
