import discord


async def banchannel(bot, ctx):
    if ctx.author.id != ctx.guild.owner.id:
        return "Due to how dangerous this command is, only the server owner can run this command."
    elif not ctx.guild.me.guild_permissions.ban_members:
        return "I don't have ban permissions!"

    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
    }
    try:
        channel = await ctx.guild.create_text_channel(
            "do-not-type-here", overwrites=overwrites
        )
    except discord.errors.Forbidden:
        return "I don't have the manage channels permission!"

    await channel.send(
        "DO NOT SAY ANYTHING IN THIS CHANNEL OR ELSE YOU **__WILL BE INSTA-BANNED. __**"
    )

    msg = await channel.send(
        f"<a:loading:883205345705619468> Adding this channel to the database... {ctx.guild.owner.mention}"
    )

    await bot.db.execute(
        "INSERT INTO banchannels(id) VALUES ($1)",
        channel.id,
    )

    await msg.edit(
        content=f"{ctx.guild.owner.mention}, the setup is successful! **Currently, @everyone cannot see this channel.** You may send more messages here, delete my messages, change the channel name or topic, or move the channel. You can also delete the channel if you don't want to have this feature anymore. __You can give everyone permissions to view this channel when you are ready.__"
    )

    return f"Done! Check out {channel.mention}"
