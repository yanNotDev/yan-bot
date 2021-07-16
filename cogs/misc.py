from discord import Embed
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, cmd=None):
        embed=Embed(description="_ _", colour=ctx.guild.me.color)
        if cmd is None:
            embed.add_field(name="Skyblock", value="`rates`, `stats`", inline=False)
            embed.add_field(name="Miscellaneous", value="`help`, `info`", inline=False)
            embed.set_footer(text="Use \"y!help command\" for more help on that command.")

        elif cmd == "rates" or cmd == "r":
            embed=Embed(title="Rates", description="Calculate coins per from farming.", colour=ctx.guild.me.color)
            embed.add_field(name="Usage", value="y!rates <ign> [profile]", inline=True)
            embed.set_footer(text="Made by yan#0069", icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif")

        elif cmd == "stats" or cmd == "s":
            embed=Embed(title="Stats", description="Shows a player's general skyblock stats.", colour=ctx.guild.me.color)
            embed.add_field(name="Usage", value="y!rates <ign> [profile]", inline=True)
            embed.set_footer(text="Made by yan#0069", icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif")

        elif cmd == "help":
            embed=Embed(title="Help", description="Displays the help message.")
            embed.add_field(name="Usage", value="y!rates help [command]", inline=True)
            embed.set_footer(text="Made by yan#0069", icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif")

        elif cmd == "info":
            embed=Embed(title="Info", description="Displays general info about the bot.", colour=ctx.guild.me.color)
            embed.add_field(name="Usage", value="y!info", inline=True)
            embed.set_footer(text="Made by yan#0069", icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif")
        
        else:
            return
        
        await ctx.send(embed=embed)


    @commands.command()
    async def info(self, ctx):
        embed=Embed(title="yan", description="idk why i made this use if you want to", colour=ctx.guild.me.color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif")
        embed.add_field(name="cool stats", value=f"**Servers**: {len(self.bot.guilds)}\n**Users**: {len(self.bot.users)}\n**Ping**: {round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="links", value=f"[**Bot Invite**](https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=278528&scope=bot%20applications.commands)\n[**Server**](https://discord.gg/hcazeVMrSN)\n[**Source Code**](https://github.com/yanNotDev/yan-bot)")
        embed.set_footer(text="Made by yan#0069", icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif")
        
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(help(bot))