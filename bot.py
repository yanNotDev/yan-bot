import asyncio
import datetime
import traceback
from os import listdir

import asyncpg
import discord
from discord.ext import commands

# from hypercorn.asyncio import serve
# from hypercorn.config import Config
# from quart import Quart, request

from util.config import *

assert discord.__version__.startswith("2"), "RUN THE SOURCE COMMAND FFS"

# app = Quart(__name__)
# config = Config()
# config.bind = ['0.0.0.0:8000']

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


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


activity = discord.Activity(
    name=f"use slash commands", type=discord.ActivityType.watching
)


class SlashBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
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

    async def setup_hook(self):
        await self.load_extension("jishaku")
        for filename in listdir("./slash-cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"slash-cogs.{filename[:-3]}")
        await self.tree.sync()


bot = SlashBot()


@bot.event
async def on_ready():
    print("yan-bot is ready aaaaa")
    # await serve(app, config)


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title="hi i am yan bot",
                description="`y!help`, `y!help command_name` for help on that command\n\
btw u can change prefix `y!help prefix`, commands are very cool (i have slash commands too so use them actually) please check them out and pls dont kick 😢",
                color=guild.me.colour,
            )
            embed.add_field(
                name="_ _",
                value="remember that you can do y!bl #channel and only mods can run commands in that channel then (do the command again to revert it)",
            )
            embed.add_field(
                name="_ _",
                value="there is also 1 moderation command (y!help banchannel)",
            )
            await channel.send(embed=embed)
            break


@bot.event
async def on_guild_remove(guild):
    await bot.db.execute("DELETE FROM guilds WHERE guild_id = $1", guild.id)


@bot.event
async def on_guild_channel_delete(channel):
    if await bot.db.fetchval(
        "SELECT EXISTS (SELECT id FROM channels WHERE id = $1)", channel.id
    ):
        await bot.db.execute("DELETE FROM channels WHERE id = $1", channel.id)

    if await bot.db.fetchval(
        "SELECT EXISTS (SELECT id FROM banchannels WHERE id = $1)", channel.id
    ):
        await bot.db.execute("DELETE FROM banchannels WHERE id = $1", channel.id)


@bot.event
async def on_typing(channel, user, when):
    if await bot.db.fetchval(
        "SELECT EXISTS (SELECT id FROM banchannels WHERE id = $1)", channel.id
    ):
        await channel.send(
            f"I see that {user.mention} is typing. This is __not__ a joke, so **do not send a message or you will be banned.**",
            delete_after=5,
        )


@bot.event
async def on_guild_role_delete(role):
    if await bot.db.fetchval(
        "SELECT EXISTS (SELECT role FROM vcroles WHERE role = $1)", role.id
    ):
        await bot.db.execute("DELETE FROM vcroles WHERE role = $1", role.id)


@bot.event
async def on_voice_state_update(member, before, after):

    role = member.guild.get_role(
        await bot.db.fetchval(
            "SELECT role FROM vcroles WHERE guild = $1", member.guild.id
        )
    )

    if before.channel is None and after.channel is not None:
        await member.add_roles(*[role])
    elif before.channel is not None and after.channel is None:
        await member.remove_roles(*[role])


@bot.listen("on_message")
async def on_msg(message: discord.message.Message):
    if await bot.db.fetchval(
        "SELECT EXISTS (SELECT id FROM banchannels WHERE id = $1)", message.channel.id
    ):
        if message.guild.me.guild_permissions.ban_members:
            try:
                await message.user.send(
                    f"You have been banned from {message.guild} for typing in #{message.channel}."
                )
            except discord.errors.Forbidden:
                pass
            finally:
                await message.guild.ban(
                    message.user,
                    reason=f"Sent a message in {message.channel.mention}",
                    delete_message_days=1,
                )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.reply("Only my owner can use this command!")
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.reply("Invalid channel!")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.reply("Invalid role!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply("Invalid member!")
    # elif isinstance(error, TypeError) or isinstance(error, commands.CheckFailure):
    #     return
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


# @app.route("/", methods=["POST"])
# async def hello():
#     body = await request.get_json()
#     command = bot.get_command('flask')
#     member = bot.get_guild(802883640286773269).get_member(int(body['id']))
#     await command.__call__(member)
#     return 'Success'


async def main():
    async with asyncpg.create_pool(
        dsn=f"postgres://{username}:{password}@{host}:{port}/{db_name}"
    ) as pool:

        async with bot:
            bot.db = pool
            await bot.start(token)


asyncio.run(main())
