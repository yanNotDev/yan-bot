from commands import banchannel, vcrole
from commands.channel import get_channels
from commands.uuid import uuid
from discord.ext import commands
from discord.ext.commands.converter import RoleConverter
from util.config import default_prefix


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=default_prefix):
        if (
            ctx.author.guild_permissions.manage_guild
            or ctx.author.id == 270141848000004097
        ):

            if prefix == "":
                await ctx.reply(
                    'Prefix cannot be blank (remember that your prefix cannot only have ")'
                )
                return

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
    async def blacklistchannel(self, ctx, channel=None):
        if (
            ctx.author.guild_permissions.manage_channels
            or ctx.author.id == 270141848000004097
        ):

            if channel is None:
                await ctx.reply("You must specify a channel or category to blacklist!")
                return

            channel = await get_channels(ctx, channel)

            if channel is None:
                await ctx.reply("Invalid channel!")
                return
            elif len(channel) == 0:
                await ctx.reply("Why are you trying to blacklist a voice channel?")
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
                        return await ctx.reply(
                            f"Non-moderators can now run commands in {i.mention} again."
                        )
                    else:
                        mentionList.append(i.mention)
                else:
                    await self.bot.db.execute(
                        "INSERT INTO channels(id) VALUES ($1)", i.id
                    )
                    if len(channel) == 1:
                        return await ctx.reply(
                            f"Only moderators can run commands in {i.mention} now."
                        )
                    else:
                        mentionList.append(i.mention)

            await ctx.reply(
                f"Non-moderators can now run commands in {(', ').join(mentionList)} again."
            ) if blacklisted else await ctx.reply(
                f"Only moderators can run commands in {(', ').join(mentionList)} now."
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

    @commands.command()
    async def banchannel(self, ctx):
        await ctx.send(await banchannel.banchannel(self.bot, ctx))

    @commands.command(aliases=["vc", "vcr"])
    async def vcrole(self, ctx, role: RoleConverter = None):
        if role is None:
            await ctx.reply("You must specify a role!")
        else:
            await ctx.reply(await vcrole.vcrole(self.bot, ctx, role))


def setup(bot):
    bot.add_cog(Database(bot))
