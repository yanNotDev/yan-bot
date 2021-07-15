from discord import Embed
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(name="help")
    async def help(self, ctx, cmd=None):
        embed=Embed(description="_ _", colour=ctx.guild.me.color)
        if cmd is None:
            embed.add_field(name="Skyblock", value="`rates`, `stats`", inline=False)
            embed.add_field(name="Miscellaneous", value="`help`", inline=False)
            embed.set_footer(text="Use \"y!help command\" for more help on that command.")
        elif cmd == "rates" or cmd == "r":
            embed=Embed(title="Rates", description="Calculate coins per from farming.", colour=ctx.guild.me.color)
            embed.add_field(name="Usage", value="y!rates <ign> [profile]", inline=True)
        elif cmd == "stats" or cmd == "s":
            embed=Embed(title="Stats", description="Shows a player's general skyblock stats.", colour=ctx.guild.me.color)
            embed.add_field(name="Usage", value="y!rates <ign> [profile]", inline=True)
        elif cmd == "help":
            embed=Embed(title="Help", description="Displays the help message.")
            embed.add_field(name="Usage", value="y!rates help [command]", inline=True)
        
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(help(bot))
