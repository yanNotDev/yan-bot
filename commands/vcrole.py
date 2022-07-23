async def vcrole(bot, ctx, role=None):
    if not ctx.user.guild_permissions.manage_roles:
        return "Missing manage roles permission!"
    elif not ctx.guild.me.guild_permissions.manage_roles:
        return "I am missing manage roles permission!"
    elif (
        role.is_default()
        or role.is_bot_managed()
        or role.is_integration()
        or role.is_premium_subscriber()
    ):
        return "You can't have that as the VC role!"
    else:
        await bot.db.execute(
            "INSERT INTO vcroles(guild, role) VALUES($1, $2) ON CONFLICT (guild) DO UPDATE SET role = $2",
            ctx.guild.id,
            role.id,
        )
        return f"I will now assign/remove {role.mention} to someone whenever they join/leave a voice channel."
        
