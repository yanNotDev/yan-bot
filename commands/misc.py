from discord import Embed
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button
from util.config import default_prefix, footer_text


def help(ctx, command):
    embed = Embed(description="_ _", colour=ctx.guild.me.color)
    try:
        ctx.prefix
    except AttributeError:
        ctx.prefix = "/"
    if command is None:
        embed.add_field(
            name="Skyblock",
            value="`rates`, `manrates`, `stats`, `calcskill`, `calccata`, `calcslayer`, `fragrun`, `bits`",
            inline=False,
        )
        embed.add_field(name="Hypixel", value="`gexp`", inline=False)
        embed.add_field(name="Minecraft", value="`mcuuid`, `link`", inline=False)
        embed.add_field(
            name="Admin",
            value="`prefix`, `blacklist`, `banchannel`, `vcrole`",
            inline=False,
        )
        embed.add_field(name="Miscellaneous", value="`help`, `info`", inline=False)
        embed.set_footer(
            text=f'Use "{ctx.prefix}help <command>" for more help on that command • Arguments with <> are mandatory, [] are optional'
        )
        buttons = [
            create_button(
                style=ButtonStyle.URL,
                label="Bot invite",
                url="https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=268714000&scope=bot%20applications.commands",
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
        return {"embed": embed, "components": [action_row]}

    command = command.lower().replace(" ", "")
    if command in ["rates", "r"]:
        embed = Embed(
            title="Rates",
            description="Calculate coins per hour from farming.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}rates <ign> [profile]")
        embed.add_field(name="Aliases", value="`rates`, `r`")

    elif command in ["manualrates", "manrates", "mr"]:
        embed = Embed(
            title="Manual Rates",
            description="Calculate coins per hour from farming.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}mr <farming fortune>")
        embed.add_field(name="Aliases", value="`manualrates`, `manrates`, `mr`")

    elif command in ["stats", "s"]:
        embed = Embed(
            title="Stats",
            description="Shows a player's general skyblock stats.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}stats <ign> [profile]")
        embed.add_field(name="Aliases", value="`stats`, `s`")

    elif command in ["calcskill", "cs"]:
        embed = Embed(
            title="CalcSkill",
            description="Checks xp for the 7 main skills required to get from level to another.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}cs <lv1> <lv2>")
        embed.add_field(name="Aliases", value="`calcskill`, `cs`")

    elif command in ["calccata", "cc"]:
        embed = Embed(
            title="CalcCata",
            description="Checks xp required to get from one Catacombs level to another.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage", value=f"{ctx.prefix}cc <lv1> <lv2> [xp from each run]"
        )
        embed.add_field(name="Aliases", value="`calccata`, `cc`")

    elif command in ["calcslayer", "csl"]:
        embed = Embed(
            title="CalcSlayer",
            description="Checks xp required to get from one slayer level to another.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage", value=f"{ctx.prefix}cc <lv1> <lv2> <slayer type> [aatrox]"
        )
        embed.add_field(name="Aliases", value="`calcslayer`, `csl`")

    elif command in ["fragloot", "fl", "fragrun", "fr"]:
        embed = Embed(
            title="FragRun",
            description="Calculates average profit from fragrunning. Defaults to 1 if number of runs isn't specified. You can optionally supply the time you finish 1 run in.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage",
            value=f"{ctx.prefix}fl <number of runs> [time in minutes for 1 run]",
        )
        embed.add_field(name="Aliases", value="`fragloot`, `fl`, `fragrun`, `fr`")
        embed.set_footer(**footer_text)

    elif command in ["bits", "bit", "b"]:
        embed = Embed(
            title="Bits",
            description="Calculates coins per bit for all auctionable items",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage",
            value=f"{ctx.prefix}bits",
        )
        embed.add_field(name="Aliases", value="`bits`, `bit`, `b`")
        embed.set_footer(**footer_text)

    elif command == "gexp":
        embed = Embed(
            title="Guild XP",
            description="Gets the Guild XP for the past 7 days.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}gexp [ign]")
        embed.set_footer(**footer_text)

    elif command in ["mcuuid", "uuid"]:
        embed = Embed(
            title="MCuuid",
            description="Get's the UUID of someone's Minecraft IGN.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}uuid <ign>")
        embed.add_field(name="Aliases", value="`mcuuid`, `uuid`")

    elif command in ["link", "bind"]:
        embed = Embed(
            title="Link",
            description="Links your Discord account to a Minecraft account. Next time you don't specify an IGN for a command that needs one, it will default to your linked IGN.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}link <ign>")
        embed.add_field(name="Aliases", value="`link`, `bind`")

    elif command == "prefix":
        embed = Embed(
            title="Prefix",
            description=f"Change the prefix. Prefix becomes `{default_prefix}` if the command is ran without arguments. If you want a prefix to have a space at the end, surround it in quotes.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}prefix [prefix]")

    elif command in ["bl", "blc", "blacklist", "blacklistchannel"]:
        embed = Embed(
            title="Blacklist channel",
            description="Blacklists the bot from a channel. Only people with manage channels permission can run commands here. If the channel is already blacklisted, it will be unblacklisted.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}bl <channel>")
        embed.add_field(
            name="Aliases", value="`bl`, `blc`, `blacklist`, `blacklistchannel`"
        )

    elif command == "banchannel":
        embed = Embed(
            title="Ban channel",
            description="Creates a channel in which anyone who speaks will be banned instantly. Useful for catching botted accounts who bomb every channel with phishing links.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}banchannel")

    elif command in ["vcrole", "vcr", "vc"]:
        embed = Embed(
            title="VCrole",
            description="Lets you choose a role that gets assigned to someone when they join a VC, and removed when they leave it.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}vcrole <role>")
        embed.add_field(name="Aliases", value="`vcrole`, `vcr`, `vc`")

    elif command == "help":
        embed = Embed(
            title="Help",
            description="Displays the help message.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}rates help [command]")
        embed.set_footer(**footer_text)

    elif command == "info":
        embed = Embed(
            title="Info",
            description="Displays general info about the bot.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"{ctx.prefix}info")

    else:
        return ValueError

    embed.set_footer(**footer_text)
    return {"embed": embed}


def info(bot, ctx):
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
        value=f"**Servers**: {len(bot.guilds)}\n**Users**: {len(bot.users)}\n**Ping**: {round(bot.latency * 1000)}ms",
        inline=True,
    )
    embed.add_field(
        name="links",
        value="[**Bot Invite**](https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=268714000&scope=bot%20applications.commands)\n\
[**Server**](https://discord.gg/hcazeVMrSN)\n\
[**Source Code**](https://github.com/yanNotDev/yan-bot)",
    )
    embed.set_footer(**footer_text)

    return embed
