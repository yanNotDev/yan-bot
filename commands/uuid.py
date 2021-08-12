import requests
from asyncpg.exceptions import NotNullViolationError


async def uuid(bot, id, ign=None):
    if ign is None:
        mcuuid = await bot.db.fetchval("SELECT uuid FROM users WHERE id = $1", id)
        if mcuuid is not None:
            return mcuuid
    else:
        ign = ign.lower()
        try:
            mcuuid = await bot.db.fetchval("SELECT uuid FROM uuids WHERE ign = $1", ign)
        except NotNullViolationError:
            pass

    if mcuuid is not None:
        return mcuuid

    if ign is None:
        return KeyError

    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
    if request.status_code == 200:
        r = request.json()

        mcuuid = r["id"]
        await bot.db.execute(
            "INSERT INTO uuids (ign, uuid) VALUES($1, $2) ON CONFLICT (uuid) DO UPDATE SET ign = $1",
            ign,
            mcuuid,
        )
        return mcuuid
    else:
        return request.status_code
