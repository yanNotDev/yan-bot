import discord
from util.config import default_prefix, footer_text


def help(ctx, command):
    embed = discord.Embed(description="_ _", colour=ctx.guild.me.color)
    if command is None:
        embed.add_field(
            name="Skyblock",
            value="`rates`, `manrates`, `stats`, `calcskill`, `calccata`, `calcslayer`, `calcpowder`, `fragrun`, `bits`",
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
            text=f'Use "/help <command>" for more help on that command • Arguments with <> are mandatory, [] are optional'
        )
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Bot invite",
                url="https://discord.com/oauth2/authorize?client_id=862232441044860938&permissions=268714000&scope=bot%20applications.commands",
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Support server", url="https://discord.gg/hcazeVMrSN"
            )
        )
        view.add_item(
            discord.ui.Button(
                label="Source code", url="https://github.com/yanNotDev/yan-bot"
            )
        )
        return {"embed": embed, "view": view}

    command = command.lower().replace(" ", "")
    if command in ["rates", "r"]:
        embed = discord.Embed(
            title="Rates",
            description="Calculate coins per hour from farming.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/rates <ign> [profile]")

    elif command in ["manualrates", "manrates", "mr"]:
        embed = discord.Embed(
            title="Manual Rates",
            description="Calculate coins per hour from farming.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/mr <farming fortune>")

    elif command in ["stats", "s"]:
        embed = discord.Embed(
            title="Stats",
            description="Shows a player's general skyblock stats.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/stats <ign> [profile]")

    elif command in ["calcskill", "cs"]:
        embed = discord.Embed(
            title="CalcSkill",
            description="Checks xp for the 7 main skills required to get from level to another.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/cs <lv1> <lv2>")

    elif command in ["calccata", "cc"]:
        embed = discord.Embed(
            title="CalcCata",
            description="Checks xp required to get from one Catacombs level to another.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage", value=f"/cc <lv1> <lv2> [xp from each run]"
        )

    elif command in ["calcslayer", "csl"]:
        embed = discord.Embed(
            title="CalcSlayer",
            description="Checks xp required to get from one slayer level to another.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage", value=f"/cc <lv1> <lv2> <slayer type> [aatrox]"
        )

    elif command in ["calcpowder", "cp", "powder"]:
        embed = discord.Embed(
            title="CalcPowder",
            description="Calculates the amount of powder needed from a start level to an end level.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage", value=f"/cp <perk> <startLevel> <endLevel>"
        )

    elif command in ["fragloot", "fl", "fragrun", "fr"]:
        embed = discord.Embed(
            title="FragRun",
            description="Calculates average profit from fragrunning. Defaults to 1 if number of runs isn't specified. You can optionally supply the time you finish 1 run in.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage",
            value=f"/fl <number of runs> [time in minutes for 1 run]",
        )
        embed.set_footer(**footer_text)

    elif command in ["bits", "bit", "b"]:
        embed = discord.Embed(
            title="Bits",
            description="Calculates coins per bit for all auctionable items",
            colour=ctx.guild.me.color,
        )
        embed.add_field(
            name="Usage",
            value=f"/bits",
        )
        embed.set_footer(**footer_text)

    elif command == "gexp":
        embed = discord.Embed(
            title="Guild XP",
            description="Gets the Guild XP for the past 7 days.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/gexp [ign]")
        embed.set_footer(**footer_text)

    elif command in ["mcuuid", "uuid"]:
        embed = discord.Embed(
            title="MCuuid",
            description="Get's the UUID of someone's Minecraft IGN.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/uuid <ign>")

    elif command in ["link", "bind"]:
        embed = discord.Embed(
            title="Link",
            description="Links your Discord account to a Minecraft account. Next time you don't specify an IGN for a command that needs one, it will default to your linked IGN.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/link <ign>")

    elif command == "prefix":
        embed = discord.Embed(
            title="Prefix",
            description=f"Change the prefix. Prefix becomes `{default_prefix}` if the command is ran without arguments. If you want a prefix to have a space at the end, surround it in quotes.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/prefix [prefix]")

    elif command in ["bl", "blc", "blacklist", "blacklistchannel"]:
        embed = discord.Embed(
            title="Blacklist channel",
            description="Blacklists the bot from a channel. Only people with manage channels permission can run commands here. If the channel is already blacklisted, it will be unblacklisted.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/bl <channel>")
        embed.add_field(
        )

    elif command == "banchannel":
        embed = discord.Embed(
            title="Ban channel",
            description="Creates a channel in which anyone who speaks will be banned instantly. Useful for catching botted accounts who bomb every channel with phishing links.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/banchannel")

    elif command in ["vcrole", "vcr", "vc"]:
        embed = discord.Embed(
            title="VCrole",
            description="Lets you choose a role that gets assigned to someone when they join a VC, and removed when they leave it.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/vcrole <role>")

    elif command == "help":
        embed = discord.Embed(
            title="Help",
            description="Displays the help message.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/rates help [command]")
        embed.set_footer(**footer_text)

    elif command == "info":
        embed = discord.Embed(
            title="Info",
            description="Displays general info about the bot.",
            colour=ctx.guild.me.color,
        )
        embed.add_field(name="Usage", value=f"/info")

    else:
        return ValueError

    embed.set_footer(**footer_text)
    return {"embed": embed}


def info(bot, ctx):
    embed = discord.Embed(
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
