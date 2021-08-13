from json import dump
from time import sleep, perf_counter

from requests import get


def update_json():
    data = get("https://moulberry.codes/lowestbin.json").json()

    with open("util/lbin/lowestbin.json", "w") as file:
        dump(data, file, indent=4)

while True:
    t1 = perf_counter()
    update_json()
    t2 = perf_counter()
    duration = t2 - t1
    print(f"Updated lowest BIN cache in {duration} seconds")
    sleep(120 - duration)
