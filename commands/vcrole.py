from discord.ext.commands.converter import RoleConverter


async def vcrole(bot, ctx, role: RoleConverter = None):
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.reply("Missing manage roles permission!")
    elif not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.reply("I am missing manage roles permission!")
    elif (
        role.is_default()
        or role.is_bot_managed()
        or role.is_integration()
        or role.is_premium_subscriber()
    ):
        await ctx.reply("You can't have that as the VC role!")
    else:
        await bot.db.execute(
            "INSERT INTO vcroles(guild, role) VALUES($1, $2) ON CONFLICT (guild) DO UPDATE SET role = $2",
            ctx.guild.id,
            role.id,
        )
        await ctx.reply(
            f"I will now assign/remove {role.mention} to someone whenever they join/leave a voice channel."
        )
