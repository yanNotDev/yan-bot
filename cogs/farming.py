from commands import rates
from discord import Embed
from discord.ext import commands
from util.config import footer_text
from commands.uuid import uuid


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["r"])
    async def rates(self, ctx, ign=None, profile=None):
        mcuuid = await uuid(self.bot, ctx.author.id, ign)
        if mcuuid == 204:
            await ctx.reply("Invalid IGN!")
            return
        elif mcuuid == KeyError:
            await ctx.reply(
                f"You must enter an ign (and optionally, a profile)!\neg `{ctx.prefix}r minikloon banana`\n\
If you're too lazy to do that, do `{ctx.prefix}help link`"
            )
        else:
            embed = Embed(
                description="If this message doesn't update within a few seconds, make sure all your API is on and your hoe is in your first hotbar slot.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="loading aaaa", value="_ _", inline=False)
            embed.set_footer(**footer_text)
            msg = await ctx.reply(embed=embed)

            embed = rates.rates(ctx, mcuuid, profile)
            await msg.edit(embed=embed)

    @commands.command(aliases=["mr", "manrates"])
    async def manualrates(self, ctx, ff=None):
        if ff is None:
            await ctx.reply(
                f"You must enter a valid integer! (no letters, decimals, etc)\neg `{ctx.prefix}mr 348`"
            )
        else:
            try:
                ff = int(ff.replace(",", ""))
            except ValueError:
                await ctx.reply("You must enter a valid integer! (no letters, decimals, etc)")

            embed = rates.manualrates(ctx, ff)
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Farming(bot))
