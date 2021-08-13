from bot import slash_blacklist
from commands import stats
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from util.config import footer_text
from commands.uuid import uuid


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
        elif mcuuid == KeyError:
            await ctx.send(
                f"Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                hidden=True,
            )
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, sorry :cry:",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="HYPIXEL WHY are you so sLOW", value="_ _", inline=False)
            embed.set_footer(**footer_text)

            hidden = await slash_blacklist(ctx)
            msg = await ctx.send(embed=embed, hidden=hidden)

            embed = stats.stats(ctx, mcuuid, profile)
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

            hidden = await slash_blacklist(ctx)
            await ctx.send(msg, hidden=hidden)


def setup(bot: commands.Bot):
    bot.add_cog(Stats(bot))
