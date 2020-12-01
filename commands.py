import urllib
import json
import datetime
import math


def command_xp(options):
    res = urllib.request.urlopen(
        "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=326460&key=7359F5150A808259B6C38735D89B910A&steamid=76561198091960570")
    jsonRes = json.loads(res.read())
    xp = ""
    for item in jsonRes["playerstats"]["stats"]:
        if item["name"] == "xp":
            xp = item["value"]
            break
    return xp


def command_hunad(options):
    return "Ich hab 577 Stunden für Level 100 und 626 Stunden für 1M XP gebraucht."


def command_afterstream(options):
    pass


def command_crossplay(options):
    return "kChamp sagt im Wortlaut: Unfortunately, crossplay isn't supported because we will be updating the game with different content and at different rates."


def command_debug(options):
    pass


def command_discord(options):
    return "https://discord.gg/Afwxq8Y"


def command_donation(options):
    return "https://www.tipeeestream.com/termpounator/donation"


def command_godgays(options):
    return "Mein God Rays-Unlock gegen den Entwickler kChamp: https://www.youtube.com/watch?v=9ZxzMyzQ594&t=12s"


def command_konsole(options):
    return "Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen"


def command_lieblingswaffe(options):
    return "Aufgrund der extremen Variabilität von Spielmodi, Distanz und Position habe ich nicht DIE eine Lieblingswaffe. Jede Waffe kann in einer bestimmten Situation gut sein."


def command_michi(options):
    alter = datetime.date.today() - datetime.date(1997, 10, 29)
    return "Michi ist {0} und studiert Maschinenbau im Master.".format(math.floor(alter.days/365.25))


def command_reddit(options):
    return "https://www.reddit.com/r/dermichi"


def command_roadto(options):
    return 2500000-int(command_xp(options))


def command_sew(options):
    return "Hier findest du Michi's Shoot Every Weapon: https://youtube.com/playlist?list=PLRL2wVgCQQsvNAPoxHWNiXjz5J6FONlgA"


def command_spielstunden(options):
    res = urllib.request.urlopen(
        "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=7359F5150A808259B6C38735D89B910A&format=json&steamid=76561198091960570"
    )
    jsonRes = json.loads(res.read())
    spielstunden = "-60"
    for game in jsonRes["response"]["games"]:
        if game["appid"] == 326460:
            spielstunden = game["playtime_forever"]
            break
    return("%.2f" % (int(spielstunden)/60.0))


def command_statistik(options):
    return "https://docs.google.com/spreadsheets/d/1mVHx01Px69b0l5vRhVRKkamsZ1aSNR9CA7sOzKt0FDQ/edit?usp=sharing SSL Statistik von Michi"


def command_sub(options):
    return "Die Kanalmitgliedschaft ist verfügbar! Je nach Stufe erhaltet ihr verschiedene Vorteile wie Discord-Rollen oder eigene Videos. weitere Infos: youtu.be/G9kQPEegHd8"


def command_tlou(options):
    return "The Last of Us II ist der direkte Nachfolger vom ersten Teil und setzt die Story fort. In dieser postapokalyptischen Welt kämpfen wir gegen Infizierte und Hunter, die uns das Leben zur Hölle machen."


def command_turnier(options):
    return "https://discord.gg/8vGVBVu"


def command_updateConsole(options):
    return "Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen"


def command_uptime(options):
    return str(options["streamAge"]-datetime.datetime.now())

# PRESET


def command_name(options):
    pass


commandNames = {"!100": command_hunad, "!afterstream": command_afterstream, "!crossplay": command_crossplay, "!debug": command_debug, "!discord": command_discord, "!donation": command_donation, "!godrays": command_godgays, "!konsole": command_konsole, "!lieblingswaffe": command_lieblingswaffe,
                "!michi": command_michi, "!reddit": command_reddit, "!roadto": command_roadto, "!sew": command_sew, "!spielstunden": command_spielstunden, "!statistik": command_statistik,  "!sub": command_sub, "!tlou": command_tlou, "!turnier": command_turnier, "!updateconsole": command_updateConsole, "!xp": command_xp}


def executeCommands(parentInputs):
    msgParts = parentInputs["message"]["snippet"]["textMessageDetails"]["messageText"].split(
        " ")
    cmd = msgParts[0]
    if cmd in commandNames.keys():
        opt = {"streamage": parentInputs["streamAge"]}
        if len(msgParts) > 1:
            parentInputs["sendText"](commandNames[cmd](opt
                                                       ), " ".join(msgParts[1:]))
        else:
            parentInputs["sendText"](commandNames[cmd](opt))
