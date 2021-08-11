import datetime
import traceback
from os import listdir

import asyncpg
import discord
from discord.ext import commands
from discord_slash import SlashCommand

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
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


async def create_db_pool():
    bot.db = await asyncpg.create_pool(
        dsn=f"postgres://{username}:{password}@{host}:{port}/{db_name}"
    )
    print(f"Successfully connected to PostGreSQL database ({db_name}).")


@bot.event
async def on_ready():
    print("yan-bot is ready aaaaa")


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="hi i am yan bot",
                description="`y!help`, `y!help command_name` for help on that command\n\
btw u can change prefix `y!help prefix`, commands are very cool please check them out and pls dont kick 😢",
                color=guild.me.colour,
            )
            embed.add_field(
                name="_ _",
                value="remember that you can do y!bl #channel and only mods can run commands in that channel then, do the command again to revert it",
            )

            await channel.send(embed=embed)
        break


@bot.event
async def on_guild_remove(guild):
    await bot.db.execute("DELETE FROM guilds WHERE guild_id = $1", guild.id)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.reply("Only my owner can use this command!")
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.reply("Invalid channel!")
    elif isinstance(error, commands.CheckFailure):
        return
    else:
        print(error)
        embed = discord.Embed(title="Command Error", colour=ctx.guild.me.color)
        embed.add_field(name="Name", value=ctx.command.qualified_name)
        embed.add_field(name="Author", value=f"{ctx.author} (ID: {ctx.author.id})")

        fmt = f"Channel: {ctx.channel} (ID: {ctx.channel.id})"
        if ctx.guild:
            fmt = f"{fmt}\nGuild: {ctx.guild} (ID: {ctx.guild.id})"

        embed.add_field(name="Location", value=fmt, inline=False)

        exc = "".join(
            traceback.format_exception(
                type(error), error, error.__traceback__, chain=False
            )
        )
        embed.description = f"```py\n{exc}\n```"
        embed.timestamp = datetime.datetime.utcnow()
        channel = bot.get_channel(860749453513981962)
        await channel.send(embed=embed)


@bot.check
async def blacklist(ctx):
    if ctx.author.id == 270141848000004097:
        return True

    if not ctx.author.guild_permissions.manage_channels:
        return not await bot.db.fetchval(
            "SELECT exists (SELECT id FROM channels WHERE id = $1)", ctx.channel.id
        )
    else:
        return True


bot.load_extension("jishaku")
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
for filename in listdir("./slash-cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"slash-cogs.{filename[:-3]}")


bot.loop.run_until_complete(create_db_pool())
bot.run(token)
