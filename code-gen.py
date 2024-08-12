# NOTES FROM CONNER:
# import only non-online cards

import os
import json
import sys
import math

allSetCodes = set()

setsInserted = set()

manaCostsInserted = {""}

legalModernSets = {"Assassin's Creed","Modern Horizons 3","Outlaws of Thunder Junction","Murders at Karlov Manor","The Lost Caverns of Ixalan","Wilds of Eldraine","The Lord of the Rings: Tales of Middle Earth","March of the Machine: The Aftermath","March of the Machine","Phyrexia: All Will Be One","The Brothers' War","Dominaria United  ","Streets of New Capenna","Kamigawa: Neon Dynasty","Innistrad: Crimson Vow","Innistrad: Midnight Hunt","Adventures in the Forgotten Realms","Modern Horizons 2","Strixhaven","Kaldheim","Zendikar Rising","Core 2021","Ikoria: Lair of Behemoths","Theros Beyond Death","Throne of Eldraine","Core Set 2020","Modern Horizons","War of the Spark","Ravnica Allegiance","Guilds of Ravnica","Core Set 2019","Dominaria","Rivals of Ixalan","Ixalan","Hour of Devastation","Amonkhet","Aether Revolt","Kaladesh","Eldritch Moon","Shadows over Innistrad","Oath of the Gatewatch","Battle for Zendikar","Magic Origins","Dragons of Tarkir","Fate Reforged","Khans of Tarkir","Magic 2015","Journey into Nyx","Born of the Gods","Theros","Magic 2014","Dragon's Maze","Gatecrash","Return to Ravnica","Magic 2013","Avacyn Restored","Dark Ascension","Innistrad","Magic 2012","New Phyrexia","Mirrodin Besieged","Scars of Mirrodin","Magic 2011","Rise of the Eldrazi","Worldwake","Zendikar","Magic 2010","Alara Reborn","Conflux","Shards of Alara","Eventide","Shadowmoor","Morningtide","Lorwyn","Tenth Edition","Future Sight","Planar Chaos","Time Spiral","Coldsnap","Dissension","Guildpact","Ravnica: City of Guilds","Ninth Edition","Saviors of Kamigawa","Eighth Edition","Betrayers of Kamigawa","Champions of Kamigawa","Fifth Dawn","Darksteel","Mirrodin"}

legalPioneerSets = {"Outlaws of Thunder Junction","Murders at Karlov Manor","The Lost Caverns of Ixalan","Wilds of Eldraine","March of the Machine: The Aftermath","March of the Machine","Phyrexia: All Will Be One","The Brothers' War","Dominaria United","Streets of New Capenna","Kamigawa: Neon Dynasty","Innistrad: Crimson Vow","Innistrad: Midnight Hunt","Adventures in the Forgotten Realms","Strixhaven","Kaldheim","Zendikar Rising","Core 2021","Ikoria Lair of Behemoths","Theros Beyond Death","Throne of Eldraine","Core Set 2020","War of the Spark","Ravnica Allegiance","Guilds of Ravnica","Core Set 2019","Dominaria","Rivals of Ixalan","Ixalan","Hour of Devastation","Amonkhet","Aether Revolt","Kaladesh","Eldritch Moon","Shadows over Innistrad","Oath of the Gatewatch","Battle for Zendikar","Magic Origins","Dragons of Tarkir","Fate Reforged","Khans of Tarkir","Magic 2015","Journey into Nyx","Born of the Gods","Theros","Magic 2014","Dragon's Maze","Gatecrash","Return to Ravnica"}

legalStandardSets = {"Outlaws of Thunder Junction","Murders at Karlov Manor","The Lost Caverns of Ixalan","Wilds of Eldraine","March of the Machine: The Aftermath","March of the Machine","Phyrexia: All Will Be One","The Brothers' War","Dominaria United","Streets of New Capenna","Kamigawa: Neon Dynasty","Innistrad: Crimson Vow","Innistrad: Midnight Hunt"}

def genAllSetCodes():
    path = "assets/sets/"

    for file in os.listdir(path):
        allSetCodes.add(file.split(".")[0])

def askPrelude():
    userInput = input("Include prelude? (yes/y or no/n): ").lower()

    while userInput not in ["yes", "y", "no", "n"]:
        print("")
        print("Invalid innput. Please try again.")
        userInput = input("Include prelude? (yes/y or no/n)").lower()

    return userInput in ["yes", "y"]


def askSetCodes():
    print("What would you like to do?")
    print("  - Single MTG set code (e.g. 'LEB')")
    print("  - Column-separated MTG set codes (e.g. 'M21, BCHR, DRK')")
    print("  - 'INSERT ALL' to insert all sets.")
    print("  - 'q' to quit.")
    userInput = input("\nInput: ")
    sets = set()
    
    while userInput != "q":
        if userInput == "INSERT ALL" and len(setsInserted) == 0:
            sets.update(allSetCodes)
            break
        elif userInput == "INSERT ALL" and len(setsInserted) != 0:
            print("Sets already have been appended to 'out.sql'")
        else:
            setList = userInput.replace(" ", "").upper().split(",")

            for code in setList:
                if code in setsInserted:
                    print(code + " already appended to 'out.sql'.")
                    sets.clear()
                    break
                elif code in allSetCodes:
                    sets.add(code)
                else:
                    print(code + " not in validified codes.")
                    sets.clear()
                    break
            else:
                break

        print("")
        userInput = input("Please try again (or q to quit): ")

    return sets

def getJSON(path):
    f = open(path)

    return json.load(f)

def lqInsertSet(json):
    s = "INSERT INTO sets (set_id, set_name, release_date) VALUES ("

    set_id       = "'" + json["code"] + "', "
    set_name     = "'" + json["name"] .replace("'", "''") + "', "
    release_date = "'" + json["releaseDate"] + "'"

    return s + set_id + set_name + release_date + ");"

def lqInsertCMC(json):
    # TODO insert ignore isn't great
    s = "INSERT INTO cmc (mana_cost, cmc) VALUES ("

    mana_cost = "'" + json["manaCost"] + "', "
    cmc       = str(math.floor(json["convertedManaCost"]))

    return s + mana_cost + cmc + ");"

def lqInsertCards(json):
    s = "INSERT INTO cards (uuid, scryfall_id, set_id, name, type, mana_cost, color, color_identity, rarity) VALUES ("
    mc = json["manaCost"] if "manaCost" in json else ""

    uuid           = "'" + json["uuid"] + "', "
    scryfall_id    = "'" + json["identifiers"]["scryfallId"] + "', "
    set_id         = "'" + json["setCode"] + "', "
    # TODO this is bad
    name           = "'" + json["name"].replace("'", "''") + "', "
    # TODO this is also bad
    type           = "'" + json["types"][0] + "', "
    mana_cost      = "'" + mc + "', "
    color          = "'" + getColorAbbrFromList(json["colors"]) + "', "
    color_identity = "'" + getColorAbbrFromList(json["colorIdentity"]) + "', "
    rarity         = "'" + json["rarity"] + "'"

    return s + uuid + scryfall_id + set_id + name + type + mana_cost + color + color_identity + rarity + ");"

def getColorAbbrFromList(l):
    s = ""

    if "W" in l: s = s + "W"
    if "U" in l: s = s + "U"
    if "B" in l: s = s + "B"
    if "R" in l: s = s + "R"
    if "G" in l: s = s + "G"

    return s

def lqInsertCreature(json):
    s = "INSERT INTO creature (uuid, power, toughness) VALUES ("

    uuid     = "'" + json["uuid"] + "', "
    power    = "'" + json["power"] + "', "
    toughness = "'" + json["toughness"] + "'"

    return s + uuid + power + toughness + ");"

def lqInsertLegality(json, set_name):
    s = "INSERT INTO legality (uuid, commander, legacy, modern, pauper, pioneer, standard, vintage) VALUES ("
    legalities = json["legalities"]

    uuid       = "'" + json["uuid"] + "', "

    commander  = "'" + legalities["commander"].lower() + "', " if "commander" in legalities else "'banned', "

    legacy     = "'" + legalities["legacy"].lower() + "', " if "legacy" in legalities else "'banned', "

    modern = ""
    if "modern" in legalities:
        modern = "'" + legalities["modern"].lower() + "', "
    elif set_name in legalModernSets:
        modern = "'legal', "
    else:
        modern = "'banned', "

    pauper = ""
    if "pauper" in legalities:
        pauper = "'" + legalities["pauper"].lower() + "', "
    elif json["rarity"] == "common":
        pauper = "'legal', "
    else:
        pauper = "'banned', "

    pioneer = ""
    if "pioneer" in legalities:
        pioneer= "'" + legalities["pioneer"].lower() + "', "
    elif set_name in legalPioneerSets:
        pioneer= "'legal', "
    else:
        pioneer= "'banned', "

    standard = ""
    if "standard" in legalities:
        standard= "'" + legalities["standard"].lower() + "', "
    elif set_name in legalStandardSets:
        standard= "'legal', "
    else:
        standard= "'banned', "

    vintage    = "'" + legalities["vintage"].lower() + "'" if "vintage" in legalities else "'banned'"

    return s + uuid + commander + legacy + modern + pauper + pioneer + standard + vintage + ");"



def writeLQCode(json, file):

    cmcInsertions      = 0
    cardInsertions     = 0
    creatureInsertions = 0
    legalityInsertions = 0

    # insert into set table 
    file.write(lqInsertSet(json))
    
    file.write("\n\n")

    # insert into cmc table
    for card in json["cards"]:
        manaCost = card["manaCost"] if "manaCost" in card else "INVALID"

        if manaCost not in manaCostsInserted and manaCost != "INVALID":
            file.write(lqInsertCMC(card) + "\n")
            manaCostsInserted.add(manaCost)
            cmcInsertions += 1

    file.write("\n\n")

    # insert into card table
    for card in json["cards"]:
        file.write(lqInsertCards(card) + "\n")
        cardInsertions += 1

    # insert into creature table
    for card in json["cards"]:
        if "power" in card and "toughness" in card:
            file.write(lqInsertCreature(card) + "\n")
            creatureInsertions += 1

    # insert into legality table
    for card in json["cards"]:
        file.write(lqInsertLegality(card, json["name"]) + "\n")
        legalityInsertions += 1

    return [cmcInsertions, cardInsertions, creatureInsertions, legalityInsertions]
        

if __name__ == '__main__':
    genAllSetCodes()
    outFile     = open("out.sql", "w")

    if askPrelude():
        prelude = open("assets/prelude.sql", "r")
        outFile.write(prelude.read())
        print("'out.sql' has been rewritten beginning with the prelude.")
        prelude.close()
    else: print("'out.sql' has been cleared, writing without prelude.")

    print("")
    userInput = askSetCodes()

    while len(userInput) > 0:


        cmcCount = cardCount = creatureCount = legalityCount = 0
        for setCode in userInput:
            with open("assets/sets/" + setCode + ".json") as setFile:
                data = json.load(setFile)

                [cmcIdx, cardIdx, creatureIdx, legalityIdx] = writeLQCode(data["data"], outFile)
                cmcCount      += cmcIdx
                cardCount     += cardIdx
                creatureCount += creatureIdx
                legalityCount += legalityIdx
                setsInserted.add(setCode)

        print("\nCode successfully appended to 'out.sql'.")
        print("cmc      TABLE insertion count = ", cmcCount)
        print("card     TABLE insertion count = ", cardCount)
        print("creature TABLE insertion count = ", creatureCount)
        print("legality TABLE insertion count = ", legalityCount)

        if len(setsInserted) == len(allSetCodes): break
        print("")
        userInput = askSetCodes()

    outFile.close()
