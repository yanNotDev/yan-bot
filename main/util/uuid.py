import requests

def uuid(ign):
    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
    r = request.json()
    return r["id"]
