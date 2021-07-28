import requests


def uuid(ign):
    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
    if request.status_code == 200:
        r = request.json()
        return r["id"]
    else:
        return request.status_code
