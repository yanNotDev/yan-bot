import discord
from commands import banchannel, vcrole
from commands.uuid import uuid
from discord import app_commands
from discord.ext import commands
from util.blacklist import slash_blacklist
from util.config import default_prefix


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        description='Prefix becomes y! if no prefix is given. Surround prefix in "" if it has spaces.',
    )
    @app_commands.describe(prefix="Prefix")
    async def prefix(self, interaction, prefix: str | None):
        prefix = prefix or default_prefix
        if (
            interaction.user.guild_permissions.manage_guild
            or interaction.user.id == 270141848000004097
        ):

            prefix = prefix.replace('"', "")

            if prefix == "":
                await interaction.response.send_message(
                    'Prefix cannot be blank (remember that your prefix cannot only have ")',
                    ephemeral=True,
                )
                return

            await self.bot.db.execute(
                'UPDATE guilds SET prefix = $1 WHERE "guild_id" = $2',
                prefix,
                interaction.guild.id,
            )
            ephemeral = await slash_blacklist(self.bot, interaction)
            if prefix == default_prefix:
                await interaction.response.send_message(
                    f"Changed prefix back to the default `{prefix}`", ephemeral=ephemeral
                )
            else:
                await interaction.response.send_message(f"Prefix changed to `{prefix}`", ephemeral=ephemeral)

        else:
            await interaction.response.send_message("Missing manage server permissions!", ephemeral=True)

    @app_commands.command(
        description="Toggle blacklist on current channel. Only people with manage channels perm can run commands here.",
    )
    @app_commands.describe(channel="Channel")
    async def blacklist(self, interaction, channel: discord.TextChannel):
        if (
            interaction.user.guild_permissions.manage_channels
            or interaction.user.id == 270141848000004097
        ):
            blacklisted = await self.bot.db.fetchval(
                "SELECT id FROM channels WHERE id = $1",
                channel.id,
            )
            if blacklisted:
                await self.bot.db.execute(
                    "DELETE FROM channels WHERE id = $1", channel.id
                )
                return await interaction.response.send_message(
                    f"Non-moderators can now run commands in {channel.mention} again."
                )
            else:
                await self.bot.db.execute(
                    "INSERT INTO channels(id) VALUES ($1)", channel.id
                )
                return await interaction.response.send_message(
                    f"Only moderators can run commands in {channel.mention} now."
                )
        else:
            await interaction.response.send_message("Missing manage channel permissions!", ephemeral=True)

    @app_commands.command(
        description="Links your Discord to a Minecraft IGN. Next time you don't specify an IGN, it will default to this.",
    )
    @app_commands.describe(ign="IGN")
    async def link(self, interaction, ign: str):
        mcuuid = await uuid(self.bot, interaction.user.id, ign.lower())
        if mcuuid == 204:
            await interaction.response.send_message("That's not a valid IGN!", ephemeral=True)
        else:
            await self.bot.db.execute(
                "INSERT INTO users(id, uuid) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET uuid = $2",
                interaction.user.id,
                mcuuid,
            )

            ephemeral = await slash_blacklist(self.bot, interaction)
            await interaction.response.send_message(f"Linked {interaction.user.mention} to {ign}", ephemeral=ephemeral)

    @app_commands.command(
        description="Sets up a channel where anyone who talks will be insta-banned. Useful for catching hacked accounts.",
    )
    async def banchannel(self, interaction):
        ephemeral = await slash_blacklist(self.bot, interaction)
        content = await banchannel.banchannel(self.bot, interaction)
        await interaction.response.send_message(content, ephemeral=ephemeral)

    @app_commands.command(
        description="Select a role that gets assigned to someone when they join a VC, and removed when they leave it.",
    )
    @app_commands.describe(role="Role")
    async def vcrole(self, interaction, role: discord.Role):
        ephemeral = await slash_blacklist(self.bot, interaction)
        content = await vcrole.vcrole(self.bot, interaction, role)
        await interaction.response.send_message(content, ephemeral=ephemeral)


async def setup(bot):
    await bot.add_cog(Database(bot))
