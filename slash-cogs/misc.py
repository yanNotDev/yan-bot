from bot import slash_blacklist
from commands import misc
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


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
                    create_choice("Ban channel", "Ban channel"),
                    create_choice("Help", "Help"),
                    create_choice("Info", "Info"),
                ],
            ),
        ],
    )
    async def help(self, ctx, command=None):
        hidden = await slash_blacklist(ctx)
        embed = misc.help(ctx, command)
        await ctx.send(**embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Displays general info about the bot.",
        # guild_ids=guilds,
    )
    async def info(self, ctx):
        embed = misc.info(self.bot, ctx)
        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)


def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
