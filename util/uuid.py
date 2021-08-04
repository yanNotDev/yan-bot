import requests


def lower(arg):
    return arg.lower()


async def uuid(bot, ign: lower):
    mcuuid = await bot.db.fetchval("SELECT uuid FROM uuids WHERE ign = $1", ign)
    if mcuuid is not None:
        return mcuuid

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
