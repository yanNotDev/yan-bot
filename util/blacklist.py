async def slash_blacklist(bot, ctx):
    if (
        ctx.user.id == 270141848000004097
        or ctx.user.guild_permissions.manage_channels
    ):
        return False
    else:
        return await bot.db.fetchval(
            "SELECT exists (SELECT id FROM channels WHERE id = $1)", ctx.channel.id
        )