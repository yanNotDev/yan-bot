from commands import misc
from discord import Embed
from discord.ext import commands
from util.config import default_prefix, footer_text


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, command=None):
        embed = misc.help(ctx, command)
        if embed == ValueError:
            await ctx.reply("That's not a command!")
        else:
            await ctx.reply(**embed)

    @commands.command()
    async def info(self, ctx):
        embed = misc.info(self.bot, ctx)
        await ctx.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
