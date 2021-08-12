from discord.ext import commands
from discord.ext.commands.errors import ChannelNotFound

async def get_channels(ctx, channel):
    channels = []
    try:  # if its a text channel
        converter = commands.TextChannelConverter()
        channel = await converter.convert(ctx, channel)
        channels.append(channel)
    except ChannelNotFound:  # if its a category
        try:
            converter = commands.CategoryChannelConverter()
            channel = await converter.convert(ctx, channel)
            for i in channel.text_channels:
                channels.append(i)
        except ChannelNotFound:  # if its not valid
            return None
    finally:
        return channels
