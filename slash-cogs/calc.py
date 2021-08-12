from bot import slash_blacklist
from commands import bits, calc, fragrun
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class SlashCalc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        description="Checks xp required to get from one Catacombs level to another.",
        # guild_ids=guilds,
        options=[
            create_option("start", "Starting level", 4, True),
            create_option("end", "Ending level", 4, True),
            create_option("xp", "XP per floor", 10, False),
        ],
    )
    async def calccata(self, ctx, start, end, xp=None):
        embed = calc.calccata(ctx, start, end, xp)
        if embed == IndexError:
            await ctx.send("You can't enter a level higher than 50!", hidden=True)
        else:
            hidden = await slash_blacklist(ctx)
            await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Checks xp required to get from one level to another, for the 7 main skills.",
        # guild_ids=guilds,
        options=[
            create_option("start", "Starting level", 4, True),
            create_option("end", "Ending level", 4, True),
        ],
    )
    async def calcskill(self, ctx, start, end):
        embed = calc.calcskill(ctx, start, end)
        if embed == IndexError:
            await ctx.send("You can't enter a level higher than 60!", hidden=True)
        else:
            hidden = await slash_blacklist(ctx)
            await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Checks xp required to get from one slayer level to another.",
        # guild_ids=guilds,
        options=[
            create_option("start", "Starting level", 4, True),
            create_option("end", "Ending level", 4, True),
            create_option(
                "type",
                "Type",
                3,
                True,
                choices=[
                    create_choice("Revenant", "Revenant"),
                    create_choice("Tarantula", "Tarantula"),
                    create_choice("Sven/Voidgloom", "Sven/Voidgloom"),
                ],
            ),
            create_option("aatrox", "Is Aatrox active", 5, False),
        ],
    )
    async def calcslayer(self, ctx, start, end, type, aatrox=False):
        embed = calc.calcslayer(ctx, start, end, type, aatrox)
        if embed == IndexError:
            await ctx.send("Slayer level can only be from 0 to 9!", hidden=True)
        else:
            hidden = await slash_blacklist(ctx)
            await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Calculates average profit from fragrunning.",
        # guild_ids=guilds,
        options=[
            create_option("runs", "Number of fragruns", 4, True),
            create_option("time", "Time in minutes to finish 1 fragrun", 10, False),
        ],
    )
    async def fragrun(self, ctx, runs, time=None):
        embed = fragrun.fragrun(ctx, runs, time)
        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)

    @cog_ext.cog_slash(
        description="Calculates coins per bit for all auctionable items.",
        # guild_ids=guilds
    )
    async def bits(self, ctx):
        embed = bits.bits(ctx)

        hidden = await slash_blacklist(ctx)
        await ctx.send(embed=embed, hidden=hidden)


def setup(bot: commands.Bot):
    bot.add_cog(SlashCalc(bot))
