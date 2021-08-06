import datetime
import traceback
from os import listdir

import asyncpg
import discord
from discord.ext import commands

from util.config import *

intents = discord.Intents.default()
intents.members = True


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(default_prefix)(bot, message)

    prefix = await bot.db.fetch(
        "SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id
    )
    if len(prefix) == 0:
        await bot.db.execute(
            "INSERT INTO guilds(guild_id, prefix) VALUES ($1, $2)",
            message.guild.id,
            default_prefix,
        )
        prefix = default_prefix
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)


activity = discord.Activity(name="y!help", type=discord.ActivityType.watching)

bot = commands.Bot(
    command_prefix=get_prefix,
    allowed_mentions=discord.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=False,
    ),
    intents=intents,
    activity=activity,
)


async def create_db_pool():
    bot.db = await asyncpg.create_pool(
        dsn=f"postgres://{username}:{password}@{host}:{port}/{db_name}"
    )
    print(f"Successfully connected to PostGreSQL database ({db_name}).")


@bot.event
async def on_ready():
    print("yan-bot is ready aaaaa")


@bot.event
async def on_guild_remove(guild):
    await bot.db.execute("DELETE FROM guilds WHERE guild_id = $1", guild.id)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.reply("Only my owner can use this command!")
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.reply("Invalid channel!")
    else:
        print(error)
        e = discord.Embed(title="Command Error", colour=ctx.guild.me.color)
        e.add_field(name="Name", value=ctx.command.qualified_name)
        e.add_field(name="Author", value=f"{ctx.author} (ID: {ctx.author.id})")

        fmt = f"Channel: {ctx.channel} (ID: {ctx.channel.id})"
        if ctx.guild:
            fmt = f"{fmt}\nGuild: {ctx.guild} (ID: {ctx.guild.id})"

        e.add_field(name="Location", value=fmt, inline=False)

        exc = "".join(
            traceback.format_exception(
                type(error), error, error.__traceback__, chain=False
            )
        )
        e.description = f"```py\n{exc}\n```"
        e.timestamp = datetime.datetime.utcnow()
        ch = bot.get_channel(860749453513981962)
        await ch.send(embed=e)

@bot.check
async def blacklist(ctx):
    if ctx.author.id == 270141848000004097:
        return True

    blacklisted_channel = await bot.db.fetch(
        "SELECT exists (SELECT id FROM channels WHERE id = $1)",
        ctx.channel.id,
    )
    if not ctx.author.guild_permissions.manage_channels:
        return not blacklisted_channel[0].get("exists")
    else:
        return True


bot.load_extension("jishaku")
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.loop.run_until_complete(create_db_pool())
bot.run(token)
