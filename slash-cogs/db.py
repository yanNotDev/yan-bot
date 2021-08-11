from bot import slash_blacklist
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from util.channel import *
from util.config import default_prefix
from util.uuid import uuid


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description='Prefix becomes y! if no prefix is given. Surround prefix in "" if it has spaces.',
        # guild_ids=guilds,
        options=[create_option("prefix", "Prefix", 3, False)],
    )
    async def prefix(self, ctx, prefix=default_prefix):
        if (
            ctx.author.guild_permissions.manage_guild
            or ctx.author.id == 270141848000004097
        ):

            prefix = prefix.replace('"', "")

            if prefix == "":
                await ctx.send(
                    'Prefix cannot be blank (remember that your prefix cannot only have ")',
                    hidden=True,
                )
                return

            await self.bot.db.execute(
                'UPDATE guilds SET prefix = $1 WHERE "guild_id" = $2',
                prefix,
                ctx.guild.id,
            )
            hidden = await slash_blacklist(ctx)
            if prefix == default_prefix:
                await ctx.send(f"Changed prefix back to the default `{prefix}`", hidden=hidden)
            else:
                await ctx.send(f"Prefix changed to `{prefix}`", hidden=hidden)

        else:
            await ctx.send("Missing manage server permissions!", hidden=True)

    @cog_ext.cog_slash(
        description="Toggle blacklist on current channel. Only people with manage channels perm can run commands here.",
        # guild_ids=guilds,
        options=[create_option("channel", "Channel", 7, True)],
    )
    async def blacklist(self, ctx, channel):
        if (
            ctx.author.guild_permissions.manage_channels
            or ctx.author.id == 270141848000004097
        ):

            channel = await get_channels(ctx, channel.mention)

            if channel is None:
                await ctx.send("Invalid channel!", hidden=True)
                return
            elif len(channel) == 0:
                await ctx.send(
                    "Why are you trying to blacklist a voice channel?", hidden=True
                )
                return

            mentionList = []
            for i in channel:
                blacklisted = await self.bot.db.fetchval(
                    "SELECT id FROM channels WHERE id = $1",
                    i.id,
                )
                if blacklisted:
                    await self.bot.db.execute(
                        "DELETE FROM channels WHERE id = $1", i.id
                    )
                    if len(channel) == 1:
                        return await ctx.send(
                            f"Non-moderators can now run commands in {i.mention} again."
                        )
                    else:
                        mentionList.append(i.mention)
                else:
                    await self.bot.db.execute(
                        "INSERT INTO channels(id) VALUES ($1)", i.id
                    )
                    if len(channel) == 1:
                        return await ctx.send(
                            f"Only moderators can run commands in {i.mention} now."
                        )
                    else:
                        mentionList.append(i.mention)

            await ctx.send(
                f"Non-moderators can now run commands in {(', ').join(mentionList)} again."
            ) if blacklisted else await ctx.send(
                f"Only moderators can run commands in {(', ').join(mentionList)} now."
            )
        else:
            await ctx.send("Missing manage channel permissions!", hidden=True)

    @cog_ext.cog_slash(
        description="Links your Discord to a Minecraft IGN. Next time you don't specify an IGN, it will default to this.",
        # guild_ids=guilds,
        options=[create_option("ign", "IGN", 3, True)],
    )
    async def link(self, ctx, ign):
        mcuuid = await uuid(self.bot, ctx.author.id, ign.lower())
        if mcuuid == 204:
            await ctx.send("That's not a valid IGN!", hidden=True)
        else:
            await self.bot.db.execute(
                "INSERT INTO users(id, uuid) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET uuid = $2",
                ctx.author.id,
                mcuuid,
            )

            hidden = await slash_blacklist(ctx)
            await ctx.send(f"Linked {ctx.author.mention} to {ign}", hidden=hidden)


def setup(bot):
    bot.add_cog(Database(bot))
