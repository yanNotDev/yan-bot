import json

from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, prefix=None):
        if (
            ctx.author.guild_permissions.manage_guild
            or ctx.author.id == 270141848000004097
        ):
            with open("json/prefixes.json", "r") as f:
                prefixes = json.load(f)

            if prefix is None:
                prefixes[str(ctx.guild.id)] = "y!"
            else:
                prefixes[str(ctx.guild.id)] = prefix

            with open("json/prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)

            if prefix is None:
                if (
                    ctx.author.id == 270141848000004097
                    and ctx.author.guild_permissions.manage_guild is False
                ):
                    await ctx.reply(
                        "yan you dont have manage perms here but i changed the prefix to `y!` anyway since ur bot owner"
                    )
                else:
                    await ctx.reply("Prefix changed back to the default `y!`")
            else:
                if (
                    ctx.author.id == 270141848000004097
                    and ctx.author.guild_permissions.manage_guild is False
                ):
                    await ctx.reply(
                        f"yan you dont have manage perms here but i changed the prefix to `{prefix}` anyway since ur bot owner"
                    )
                else:
                    await ctx.reply(f"Prefix changed to the `{prefix}`")
        else:
            await ctx.reply("Missing manage server permissions!")


def setup(bot):
    bot.add_cog(Admin(bot))
