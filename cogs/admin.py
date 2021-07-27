from discord.ext import commands
from util.config import default_prefix


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=None):
        if (
            ctx.author.guild_permissions.manage_guild
            or ctx.author.id == 270141848000004097
        ):
            if prefix is None:
                prefix = default_prefix

            await self.bot.db.execute(
                'UPDATE guilds SET prefix = $1 WHERE "guild_id" = $2',
                prefix,
                ctx.guild.id,
            )

            if prefix == default_prefix:
                await ctx.reply(f"Changed prefix back to the default `{prefix}`")
            else:
                await ctx.reply(f"Prefix changed to `{prefix}`")

        else:
            await ctx.reply("Missing manage server permissions!")


def setup(bot):
    bot.add_cog(Admin(bot))
