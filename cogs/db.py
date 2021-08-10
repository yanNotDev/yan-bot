from discord.channel import TextChannel
from discord.ext import commands
from util.config import default_prefix
from util.uuid import uuid


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=None):
        if (
            ctx.author.guild_permissions.manage_guild
            or ctx.author.id == 270141848000004097
        ):
            if prefix is None:
                prefix = default_prefix

            await self.bot.db.execute(
                'UPDATE guilds SET prefix = $1 WHERE "guild_id" = $2',
                prefix,
                ctx.guild.id,
            )

            if prefix == default_prefix:
                await ctx.reply(f"Changed prefix back to the default `{prefix}`")
            else:
                await ctx.reply(f"Prefix changed to `{prefix}`")

        else:
            await ctx.reply("Missing manage server permissions!")

    @commands.command(aliases=["bl", "blc", "blacklist"])
    async def blacklistchannel(self, ctx, channel: TextChannel = None):
        if (
            ctx.author.guild_permissions.manage_channels
            or ctx.author.id == 270141848000004097
        ):
            if channel is None:
                await ctx.reply("You must specify a channel to blacklist!")
                return
            else:
                blacklisted = await self.bot.db.fetch(
                    "SELECT exists (SELECT id FROM channels WHERE id = $1)",
                    channel.id,
                )
                if blacklisted[0].get("exists"):
                    await self.bot.db.execute(
                        "DELETE FROM channels WHERE id = $1", channel.id
                    )
                    await ctx.reply(
                        f"Non-moderators can now run commands in {channel.mention} again."
                    )
                    return
                else:
                    await self.bot.db.execute(
                        "INSERT INTO channels(id) VALUES ($1)", channel.id
                    )
                    await ctx.reply(
                        f"Only moderators can run commands in {channel.mention} now."
                    )

        else:
            await ctx.reply("Missing manage channel permissions!")

    @commands.command(aliases=["bind"])
    async def link(self, ctx, ign=None):
        if ign is None:
            await ctx.reply("You must specify an IGN to link your account to.")
            return

        mcuuid = await uuid(self.bot, ctx.author.id, ign.lower())

        if mcuuid == 204:
            await ctx.reply("That's not a valid IGN!")
        else:
            await self.bot.db.execute(
                "INSERT INTO users(id, uuid) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET uuid = $2",
                ctx.author.id,
                mcuuid,
            )
            await ctx.reply(f"Linked {ctx.author.mention} to {ign}")


def setup(bot):
    bot.add_cog(Database(bot))