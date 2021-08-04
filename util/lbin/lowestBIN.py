# Copyright 2020-21 Quantizr
# This file is used as part of Danker's Skyblock Mod (DSM). (Github: <https://github.com/bowser0000/SkyblockMod/>)
# DSM  is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# DSM is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with DSM.  If not, see <https://www.gnu.org/licenses/>.


import base64

# import concurrent.futures
import io
import json
import re
import time

import nbt
from requests import get
from util.config import key


def decode_nbt(raw):
    data = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(raw)))
    output = str(data["i"].tags[0]["tag"]["ExtraAttributes"]["id"]).replace(":", "-")
    if output == "PET":
        petInfo = str(data["i"].tags[0]["tag"]["ExtraAttributes"]["petInfo"])
        petInfo = json.loads(petInfo)
        output = output + "-" + str(petInfo["type"]) + "-" + str(petInfo["tier"])
    elif output == "ENCHANTED_BOOK":
        enchantments = str(data["i"].tags[0]["tag"]["ExtraAttributes"]["enchantments"])
        enchantments = (
            enchantments[1:-1]
            .replace("TAG_Int('", "")
            .replace("'): ", "")
            .upper()
            .split(", ")
        )
        enchantments.sort()
        if len(enchantments) <= 2:
            for enchant in enchantments:
                output += "-" + enchant
        else:
            output += "-" + str(len(enchantments)) + "ENCHANTS"
    elif output == "POTION":
        potion = str(data["i"].tags[0]["tag"]["display"]["Name"])
        potion = re.sub("§.", "", potion).replace(" ", "_").upper()
        output = potion
    return output


def update_json():
    start_time = time.time()
    auctions = []
    pages = get(f"https://api.hypixel.net/skyblock/auctions?key={key}").json()

    for page in range(pages["totalPages"] + 1):  # range(1): #
        getPage = get(f"https://api.hypixel.net/skyblock/auctions?page={page}&key={key}").json()
        try:
            auctions += getPage["auctions"]
        except KeyError as k:
            pass
            # print(k)
        # if page == pages["totalPages"] or page % 20 == 0:
        # print(str(page) + "/" + str(pages["totalPages"]) + " pages")

    items = []
    # totalItems = 0

    for auction in auctions:
        try:
            if auction["bin"]:
                items.append(
                    [decode_nbt(auction["item_bytes"]), auction["starting_bid"]]
                )
                # totalItems += 1
                # if totalItems % 5000 == 0:
                #     print(str(totalItems) + "/? items")
        except KeyError:
            pass

    # print(str(totalItems) + "/" + str(totalItems) + " items")
    """
  def load_items(auction):
      try:
          if auction["bin"]:
            data = nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(auction["item_bytes"])))
            for line in data.pretty_tree().splitlines():
              if "TAG_String('id'): " in line:
                output = re.sub("^.*TAG_String\('id'\): ","", line).strip()
            items.append([output, auction["starting_bid"]])
            global totalItems
            totalItems += 1
            print(totalItems)
      except KeyError:
          pass

  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(load_items, auction) for auction in auctions]
  """

    sortedItems = dict(sorted(items, key=lambda x: int(x[1]), reverse=True))

    # bazaar = get(f"https://api.hypixel.net/skyblock/bazaar?key={key}").json()["products"]
    # HPB = ', "HOT_POTATO_BOOK": ' + str(
    #     round(
    #         (
    #             bazaar["HOT_POTATO_BOOK"]["quick_status"]["sellPrice"]
    #             + bazaar["HOT_POTATO_BOOK"]["quick_status"]["buyPrice"]
    #         )
    #         / 2
    #     )
    # )
    # FPB = ', "FUMING_POTATO_BOOK": ' + str(
    #     round(
    #         (
    #             bazaar["FUMING_POTATO_BOOK"]["quick_status"]["sellPrice"]
    #             + bazaar["FUMING_POTATO_BOOK"]["quick_status"]["buyPrice"]
    #         )
    #         / 2
    #     )
    # )
    # RECOMB = ', "RECOMBOBULATOR_3000": ' + str(
    #     round(
    #         (
    #             bazaar["RECOMBOBULATOR_3000"]["quick_status"]["sellPrice"]
    #             + bazaar["RECOMBOBULATOR_3000"]["quick_status"]["buyPrice"]
    #         )
    #         / 2
    #     )
    # )
    # print("Retrieved Bazaar prices for HPB, FPB, RECOMB")

    # print(f"{HPB}\n{FPB}\n{RECOMB}")

    with open("util/lbin/lowestbin.json", "w") as f:
        json.dump(sortedItems, f, indent=4)

    print("--- %s seconds ---" % (time.time() - start_time))


while True:
    update_json()
    time.sleep(100)