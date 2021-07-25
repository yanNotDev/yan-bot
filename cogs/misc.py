from discord import Embed
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, cmd=None):
        embed = Embed(description="_ _", colour=ctx.guild.me.color)
        if cmd is None:
            embed.add_field(
                name="Skyblock",
                value="`rates`, `manrates`, `stats`, `calcskill`, `calccata`, `calcslayer`",
                inline=False,
            )
            embed.add_field(name="Admin", value="`prefix`", inline=False)
            embed.add_field(name="Miscellaneous", value="`help`, `info`", inline=False)
            embed.set_footer(
                text=f'Use "{ctx.prefix}help command" for more help on that command.'
            )

        elif cmd in ["rates", "r"]:
            embed = Embed(
                title="Rates",
                description="Calculate coins per hour from farming.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}rates <ign> [profile]")
            embed.add_field(name="Aliases", value="`rates`, `r`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd in ["manualrates", "manrates", "mr"]:
            embed = Embed(
                title="Manual Rates",
                description="Calculate coins per hour from farming.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}mr <farming fortune>")
            embed.add_field(name="Aliases", value="`manualrates`, `manrates`, `mr`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd in ["stats", "s"]:
            embed = Embed(
                title="Stats",
                description="Shows a player's general skyblock stats.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}stats <ign> [profile]")
            embed.add_field(name="Aliases", value="`stats`, `s`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd in ["calcskill", "cs"]:
            embed = Embed(
                title="CalcSkill",
                description="Checks xp for the 7 main skills required to get from level to another.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}cs <lv1> <lv2>")
            embed.add_field(name="Aliases", value="`calcskill`, `cs`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd in ["calccata", "cc"]:
            embed = Embed(
                title="CalcCata",
                description="Checks xp required to get from one Catacombs level to another.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(
                name="Usage", value=f"{ctx.prefix}cc <lv1> <lv2> [xp from each run]"
            )
            embed.add_field(name="Aliases", value="`calccata`, `cc`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd in ["calcslayer", "csl"]:
            embed = Embed(
                title="CalcSlayer",
                description="Checks xp required to get from one slayer level to another.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(
                name="Usage", value=f"{ctx.prefix}cc <lv1> <lv2> <slayer type>"
            )
            embed.add_field(name="Aliases", value="`calcslayer`, `csl`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd == "prefix":
            embed = Embed(
                title="Prefix",
                description="Change the prefix. Prefix becomes `y!` if the command is ran without arguments. If you want a prefix to have a space at the end, surround it in quotes.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}prefix <prefix>")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd == "help":
            embed = Embed(
                title="Help",
                description="Displays the help message.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}rates help [command]")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif cmd == "info":
            embed = Embed(
                title="Info",
                description="Displays general info about the bot.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value=f"{ctx.prefix}info")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        else:
            await ctx.reply("That's not a command!")
            return

        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        embed = Embed(
            title="yan",
            description="A skyblock bot. Since I'm bad, you can expect a lot of bugs (please report them by dm'ing me).",
            colour=ctx.guild.me.color,
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif"
        )
        embed.add_field(
            name="cool stats",
            value=f"**Servers**: {len(self.bot.guilds)}\n**Users**: {len(self.bot.users)}\n**Ping**: {round(self.bot.latency * 1000)}ms",
            inline=True,
        )
        embed.add_field(
            name="links",
            value=f"[**Bot Invite**](https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=278528&scope=bot%20applications.commands)\n[**Server**](https://discord.gg/hcazeVMrSN)\n[**Source Code**](https://github.com/yanNotDev/yan-bot)",
        )
        embed.set_footer(
            text="Made by yan#0069",
            icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
        )

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(help(bot))
