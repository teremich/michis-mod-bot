import urllib
import json
import datetime
# TODO: Afterstream, debug, roadto, spielstunden
commandNames = {"!100": command_hunad, "!afterstream": command_afterstream, "!crossplay": command_crossplay, "!debug": command_debug, "!discord": command_discord, "!donation": command_donation, "!godrays": command_godgays, "!konsole": command_konsole, "!lieblingswaffe": command_lieblingswaffe,
                "!michi": command_michi, "!reddit": command_reddit, "!roadto": command_roadto, "!sew": command_sew, "!spielstunden": command_spielstunden, "!statistik": command_statistik,  "!sub": command_sub, "!tlou": command_tlou, "!turnier": command_turnier, "!updateconsole": command_updateConsole, "!xp": command_xp}


def command_xp(parentInputs, msg):
    command = "!xp"
    if command == msg["snippet"]["textMessageDetails"]["messageText"][:len(command)]:
        res = urllib.request.urlopen(
            "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=326460&key=7359F5150A808259B6C38735D89B910A&steamid=76561198091960570")
        jsonRes = json.loads(res.read())
        xp = ""
        print(jsonRes)
        for item in jsonRes["playerstats"]["stats"]:
            if item["name"] == "xp":
                xp = item["value"]
                break
        parentInputs["sendText"](xp, msg["authorDetails"]["displayName"])


def command_hunad(parentInputs, msg):
    parentInputs["sendText"]("Ich hab 577 Stunden für Level 100 und 626 Stunden für 1M XP gebraucht.",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_afterstream(parentInputs, msg):
    pass


def command_crossplay(parentInputs, msg):
    parentInputs["sendText"]("kChamp sagt im Wortlaut: Unfortunately, crossplay isn't supported because we will be updating the game with different content and at different rates.",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_debug(parentInputs, msg):
    pass


def command_discord(parentInputs, msg):
    parentInputs["sendText"]("https://discord.gg/Afwxq8Y",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_donation(parentInputs, msg):
    parentInputs["sendText"]("https://www.tipeeestream.com/termpounator/donation",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_godgays(parentInputs, msg):
    parentInputs["sendText"]("Mein God Rays-Unlock gegen den Entwickler kChamp: https://www.youtube.com/watch?v=9ZxzMyzQ594&t=12s",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_konsole(parentInputs, msg):
    parentInputs["sendText"]("Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_lieblingswaffe(parentInputs, msg):
    parentInputs["sendText"]("Aufgrund der extremen Variabilität von Spielmodi, Distanz und Position habe ich nicht DIE eine Lieblingswaffe. Jede Waffe kann in einer bestimmten Situation gut sein.",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_michi(parentInputs, msg):
    alter = datetime.date.today() - datetime.date(1998, 10, 29)
    parentInputs["sendText"]("Michi ist {0} und studiert Maschinenbau im Master.".format(alter.days//365.25),
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_reddit(parentInputs, msg):
    parentInputs["sendText"]("https://www.reddit.com/r/dermichi",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_roadto(parentInputs, msg):
    # parentInputs["sendText"]("https://www.reddit.com/r/dermichi",
    #                          msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])
    pass


def command_sew(parentInputs, msg):
    parentInputs["sendText"]("Hier findest du Michi's Shoot Every Weapon: https://youtube.com/playlist?list=PLRL2wVgCQQsvNAPoxHWNiXjz5J6FONlgA",
                             msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[1:])


def command_spielstunden(parentInputs, msg):
    pass


def command_statistik(parentInputs, msg):
    pass


def command_sub(parentInputs, msg):
    pass


def command_tlou(parentInputs, msg):
    pass


def command_turnier(parentInputs, msg):
    pass


def command_updateConsole(parentInputs, msg):
    pass

# PRESET


def command_name(parentInputs, msg):
    command = "!"


def executeCommands(parentInputs, msg):
    cmd = msg["snippet"]["textMessageDetails"]["messageText"].split(" ")[0]
    if cmd in commandNames.keys():
        commandNames[cmd](parentInputs, msg)
