from bot import slash_blacklist
from commands import rates
from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from util.config import footer_text
from commands.uuid import uuid


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description="Calculate coins per hour from farming.",
        # guild_ids=guilds,
        options=[
            create_option("ign", "IGN", 3, False),
            create_option("profile", "IGN", 3, False),
        ],
    )
    async def rates(self, ctx, ign=None, profile=None):
        mcuuid = await uuid(self.bot, ctx.author.id, ign)
        if mcuuid == 204:
            await ctx.send("Invalid IGN!", hidden=True)
            return
        elif mcuuid == KeyError:
            await ctx.send(
                "Looks like you didn't specify an IGN! If you don't want to specify an IGN, check out the link command or `/link`",
                hidden=True,
            )
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, make sure all your API is on and your hoe is in your first hotbar slot.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="loading aaaa", value="_ _", inline=False)
            embed.set_footer(**footer_text)
            hidden = await slash_blacklist(ctx)
            msg = await ctx.send(embed=embed, hidden=hidden)

            embed = rates.rates(ctx, mcuuid, profile)
            await msg.edit(embed=embed)

    @cog_ext.cog_slash(
        description="Calculate coins per hour from farming.",
        # guild_ids=guilds,
        options=[
            create_option("ff", "Farming Fortune", 4, True),
        ],
    )
    async def manualrates(self, ctx, ff):
        hidden = await slash_blacklist(ctx)

        embed = rates.manualrates(ctx, ff)

        await ctx.send(embed=embed, hidden=hidden)


def setup(bot):
    bot.add_cog(Farming(bot))
