import discord
from discord.ext import commands
from os import listdir
# from dislash import *
from util.config import token

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="y!",
    allowed_mentions=discord.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=False,
    ),
    intents=intents,
)

# slash = SlashClient(bot)
# guilds = [802883640286773269, 860747004459745300, 860319342881144853, 812449183415795712, 836279047486439505]


@bot.event
async def on_ready():
    print("yan")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="y!help")
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.reply("Only my owner can use this command!")


bot.load_extension("jishaku")
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)
