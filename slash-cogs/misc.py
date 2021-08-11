from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_actionrow, create_button
from util.config import default_prefix, footer_text


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @cog_ext.cog_slash(
        description="Displays the help message.",
        # guild_ids=guilds,
        options=[
            create_option(
                "command",
                "Command name",
                3,
                False,
                choices=[
                    create_choice("Rates", "Rates"),
                    create_choice("Manaul Rates", "Manual rates"),
                    create_choice("Stats", "Stats"),
                    create_choice("Calc Skill", "Calc Skill"),
                    create_choice("Calc Cata", "Calc Cata"),
                    create_choice("Calc Slayer", "Calc Slayer"),
                    create_choice("Fragrun", "Fragrun"),
                    create_choice("Bits", "Bits"),
                    create_choice("MCuuid", "MCuuid"),
                    create_choice("Link", "Link"),
                    create_choice("Prefix", "Prefix"),
                    create_choice("Blacklist", "Blacklist"),
                    create_choice("Help", "Help"),
                    create_choice("Info", "Info"),
                ],
            ),
        ],
    )
    async def help(self, ctx, command=None):
        embed = Embed(description="_ _", colour=ctx.guild.me.color)
        if command is None:
            embed.add_field(
                name="Skyblock",
                value="`rates`, `manrates`, `stats`, `calcskill`, `calccata`, `calcslayer`, `fragloot`, `bits`",
                inline=False,
            )
            embed.add_field(name="Minecraft", value="`mcuuid`, `link`", inline=False)
            embed.add_field(name="Admin", value="`prefix`, `blacklist`", inline=False)
            embed.add_field(name="Miscellaneous", value="`help`, `info`", inline=False)
            embed.set_footer(
                text='Use "/help <command>" for more help on that command • Arguments with <> are mandatory, [] are optional'
            )

            buttons = [
                create_button(
                    style=ButtonStyle.URL,
                    label="Bot invite",
                    url="https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=278528&scope=bot%20applications.commands",
                ),
                create_button(
                    style=ButtonStyle.URL,
                    label="Support server",
                    url="https://discord.gg/hcazeVMrSN",
                ),
                create_button(
                    style=ButtonStyle.URL,
                    label="Source code",
                    url="https://github.com/yanNotDev/yan-bot",
                ),
            ]
            action_row = create_actionrow(*buttons)

            await ctx.send(embed=embed, components=[action_row])

        elif command == "Rates":
            embed = Embed(
                title="Rates",
                description="Calculate coins per hour from farming.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/rates <ign> [profile]")
            embed.add_field(name="Aliases", value="`rates`, `r`")

        elif command == "Manual Rates":
            embed = Embed(
                title="Manual Rates",
                description="Calculate coins per hour from farming.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/mr <farming fortune>")
            embed.add_field(name="Aliases", value="`manualrates`, `manrates`, `mr`")

        elif command == "Stats":
            embed = Embed(
                title="Stats",
                description="Shows a player's general skyblock stats.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/stats <ign> [profile]")
            embed.add_field(name="Aliases", value="`stats`, `s`")

        elif command == "Calc Skill":
            embed = Embed(
                title="CalcSkill",
                description="Checks xp for the 7 main skills required to get from level to another.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/cs <lv1> <lv2>")
            embed.add_field(name="Aliases", value="`calcskill`, `cs`")

        elif command == "Calc Cata":
            embed = Embed(
                title="CalcCata",
                description="Checks xp required to get from one Catacombs level to another.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/cc <lv1> <lv2> [xp from each run]")
            embed.add_field(name="Aliases", value="`calccata`, `cc`")

        elif command == "Calc Slayer":
            embed = Embed(
                title="CalcSlayer",
                description="Checks xp required to get from one slayer level to another.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(
                name="Usage", value="/cc <lv1> <lv2> <slayer type> [aatrox]"
            )
            embed.add_field(name="Aliases", value="`calcslayer`, `csl`")

        elif command == "Fragrun": 
            embed = Embed(
                title="FragLoot",
                description="Calculates average profit from fragrunning. Defaults to 1 if number of runs isn't specified. You can optionally supply the time you finish 1 run in.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(
                name="Usage",
                value="/fl <number of runs> [time in minutes for 1 run]",
            )
            embed.add_field(name="Aliases", value="`fragloot`, `fl`, `fragrun`, `fr`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif command == "Bits":
            embed = Embed(
                title="Bits",
                description="Calculates coins per bit for all auctionable items",
                colour=ctx.guild.me.color,
            )
            embed.add_field(
                name="Usage",
                value="/bits",
            )
            embed.add_field(name="Aliases", value="`bits`, `bit`, `b`")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gi",
            )

        elif command == "MCuuid":
            embed = Embed(
                title="MCuuid",
                description="Get's the UUID of someone's Minecraft IGN.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/uuid <ign>")
            embed.add_field(name="Aliases", value="`mcuuid`, `uuid`")

        elif command == "Link":
            embed = Embed(
                title="Link",
                description="Links your Discord account to a Minecraft account. Next time you don't specify an IGN for a command that needs one, it will default to your linked IGN.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/link <ign>")
            embed.add_field(name="Aliases", value="`link`, `bind`")

        elif command == "Prefix":
            embed = Embed(
                title="Prefix",
                description=f"Change the prefix. Prefix becomes `{default_prefix}` if the command is ran without arguments. If you want a prefix to have a space at the end, surround it in quotes.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/prefix [prefix]")

        elif command == "Blacklist":
            embed = Embed(
                title="Blacklist channel",
                description="Blacklists the bot from a channel. Only people with manage channels permission can run commands here. If the channel is already blacklisted, it will be unblacklisted.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/bl <channel>")
            embed.add_field(
                name="Aliases", value="`bl`, `blc`, `blacklist`, `blacklistchannel`"
            )

        elif command == "Help":
            embed = Embed(
                title="Help",
                description="Displays the help message.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/help [command]")
            embed.set_footer(
                text="Made by yan#0069",
                icon_url="https://cdn.discordapp.com/avatars/270141848000004097/a_6022d1ac0f1f2b9f9506f0eb06f6eaf0.gif",
            )

        elif command == "Info":
            embed = Embed(
                title="Info",
                description="Displays general info about the bot.",
                colour=ctx.guild.me.color,
            )
            embed.add_field(name="Usage", value="/info")

        if command is not None:
            embed.set_footer(**footer_text)
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        description="Displays general info about the bot.",
        # guild_ids=guilds,
    )
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
            value="[**Bot Invite**](https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=278528&scope=bot%20applications.commands)\n\
[**Server**](https://discord.gg/hcazeVMrSN)\n\
[**Source Code**](https://github.com/yanNotDev/yan-bot)",
        )
        embed.set_footer(**footer_text)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
