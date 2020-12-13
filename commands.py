import urllib
import json
import datetime
import math

# TODO: !filter, !listen, !quote, !afterstream, rest testen


def command_xp(options):
    res = urllib.request.urlopen(
        "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=326460&key=7359F5150A808259B6C38735D89B910A&steamid=76561198091960570")
    jsonRes = json.loads(res.read())
    xp = ""
    for item in jsonRes["playerstats"]["stats"]:
        if item["name"] == "xp":
            xp = item["value"]
            break
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> "+str(xp)
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> "+str(xp)


def command_hunad(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Michi hat 577 Stunden für Level 100 und 626 Stunden für 1M XP gebraucht."
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Michi hat 577 Stunden für Level 100 und 626 Stunden für 1M XP gebraucht."


def command_afterstream(options):
    pass


def command_crossplay(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> kChamp sagt im Wortlaut: Unfortunately, crossplay isn't supported because we will be updating the game with different content and at different rates."
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> kChamp sagt im Wortlaut: Unfortunately, crossplay isn't supported because we will be updating the game with different content and at different rates."


def command_debug(options):
    pass


def command_discord(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> https://discord.gg/Afwxq8Y"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> https://discord.gg/Afwxq8Y"


def command_donation(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> https://www.tipeeestream.com/termpounator/donation"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> https://www.tipeeestream.com/termpounator/donation"


def command_filter(options):
    # WARNING: If you type "!filter remove" and then a substring of a filtered word in chat, the filtered word will be removed!
    toParse = options["message"].split(" ")
    print(toParse, options)
    if toParse[1] == "add" and options["isMod"]:
        with open("filter.txt", "a", encoding="utf-8") as f:
            f.write("\n" + " ".join(toParse[2:]).lower())
        return "successfully added '"+" ".join(toParse[2:])+"' to the filter"
    elif toParse[1] == "remove" and options["isMod"]:
        print("trying to remove something")
        with open("filter.txt", "r+", encoding="utf-8") as f:
            ret = "successfully removed "
            for line in f:
                print(line)
                if " ".join(toParse[2:]).lower() in line:
                    ret += line + ", "
                    line = ""
            return ret
    elif options["isMod"]:
        return options["username"] + " -> Error! Syntax for this command: !filter <add|remove> <expression>"
    else:
        return options["username"] + " -> du bist kein Mod"


def command_godgays(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Mein God Rays-Unlock gegen den Entwickler kChamp: https://www.youtube.com/watch?v=9ZxzMyzQ594&t=12s"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Mein God Rays-Unlock gegen den Entwickler kChamp: https://www.youtube.com/watch?v=9ZxzMyzQ594&t=12s"


def command_konsole(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen"


def command_lieblingswaffe(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Aufgrund der extremen Variabilität von Spielmodi, Distanz und Position hat Michi nicht DIE eine Lieblingswaffe. Jede Waffe kann in einer bestimmten Situation gut sein."
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Aufgrund der extremen Variabilität von Spielmodi, Distanz und Position hat Michi nicht DIE eine Lieblingswaffe. Jede Waffe kann in einer bestimmten Situation gut sein."


def command_listen(options):
    # WARNING: If you type "!listen remove" and then a substring of a word thats being listened for in chat, this word will be removed!
    toParse = options["message"].split(" ")
    print(toParse)
    if toParse[1] == "add" and options["isMod"]:
        with open("listen.txt", "a", encoding="utf-8") as f:
            f.write("\n" + toParse[2] + ":" + " ".join(toParse[3:]).lower())
        return "successfully added '"+toParse[2]+"' to the listen list"
    elif toParse[1] == "remove" and options["isMod"]:
        with open("listen.txt", "r+", encoding="utf-8") as f:
            ret = "successfully removed "
            for line in f:
                if " ".join(toParse[2:]).lower() in line.split(":")[0]:
                    ret += line.split(":")[0] + ", "
                    line = ""
            return ret
    elif options["isMod"]:
        return options["username"] + " -> Error! Syntax for this command: !listen <add|remove> <word> <response expression>"
    else:
        return options["username"] + " -> du bist kein Mod"


def command_michi(options):
    alter = datetime.date.today() - datetime.date(1997, 10, 29)
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Michi ist {0} und studiert Maschinenbau im Master. Mehr Infos zum Studium findet ihr in der Uni-Talk Playlist".format(math.floor(alter.days/365.25))
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Michi ist {0} und studiert Maschinenbau im Master. Mehr Infos zum Studium findet ihr in der Uni-Talk Playlist".format(math.floor(alter.days/365.25))


def command_reddit(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> https://www.reddit.com/r/dermichi"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> https://www.reddit.com/r/dermichi"


def command_roadto(options):
    res = urllib.request.urlopen(
        "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=326460&key=7359F5150A808259B6C38735D89B910A&steamid=76561198091960570")
    jsonRes = json.loads(res.read())
    xp = ""
    for item in jsonRes["playerstats"]["stats"]:
        if item["name"] == "xp":
            xp = item["value"]
            break
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> "+str(2500000-int(xp))
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> "+str(2500000-int(xp))


def command_sew(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Hier findest du Michi's Shoot Every Weapon: https://youtube.com/playlist?list=PLRL2wVgCQQsvNAPoxHWNiXjz5J6FONlgA"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Hier findest du Michi's Shoot Every Weapon: https://youtube.com/playlist?list=PLRL2wVgCQQsvNAPoxHWNiXjz5J6FONlgA"


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
    if len(options["message"].split(" ")) < 2:
        return options["username"] + (" -> %.2f" % (int(spielstunden)/60.0))
    else:
        return " ".join(options["message"].split(" ")[1:])+(" -> %.2f" % (int(spielstunden)/60.0))


def command_statistik(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> https://docs.google.com/spreadsheets/d/1mVHx01Px69b0l5vRhVRKkamsZ1aSNR9CA7sOzKt0FDQ/edit?usp=sharing SSL Statistik von Michi"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> https://docs.google.com/spreadsheets/d/1mVHx01Px69b0l5vRhVRKkamsZ1aSNR9CA7sOzKt0FDQ/edit?usp=sharing SSL Statistik von Michi"


def command_sub(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Die Kanalmitgliedschaft ist verfügbar! Je nach Stufe erhaltet ihr verschiedene Vorteile wie Discord-Rollen oder eigene Videos. weitere Infos: youtu.be/G9kQPEegHd8"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Die Kanalmitgliedschaft ist verfügbar! Je nach Stufe erhaltet ihr verschiedene Vorteile wie Discord-Rollen oder eigene Videos. weitere Infos: youtu.be/G9kQPEegHd8"


def command_timemeout(options):
    print("strike reason: command_timemeout")
    options["strike"](options["userId"])
    return options["username"] + " -> Du wolltest es so!"


def command_tlou(options):
    return "The Last of Us II ist der direkte Nachfolger vom ersten Teil und setzt die Story fort. In dieser postapokalyptischen Welt kämpfen wir gegen Infizierte und Hunter, die uns das Leben zur Hölle machen."


def command_turnier(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> https://discord.gg/8vGVBVu"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> https://discord.gg/8vGVBVu"


def command_twitch(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Hier ein ausführlicher Post, warum Michi nicht auf Twitch streamt: https://www.youtube.com/post/UgxOrW9vKASAf8LUb1J4AaABCQ"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Hier ein ausführlicher Post, warum Michi nicht auf Twitch streamt: https://www.youtube.com/post/UgxOrW9vKASAf8LUb1J4AaABCQ"


def command_updateConsole(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> Michi hat keine Informationen zur Entwicklung von SSL auf jeglichen Konsolen"


def command_uptime(options):
    print(datetime.datetime.utcnow()-options["streamAge"])
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> " + str(datetime.datetime.utcnow()-options["streamAge"]).split(".")[0]
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> " + str(datetime.datetime.utcnow()-options["streamAge"]).split(".")[0]

# PRESET


def command_name(options):
    if len(options["message"].split(" ")) < 2:
        return options["username"] + " -> "  # + "TEXT"
    else:
        return " ".join(options["message"].split(" ")[1:])+" -> " + "TEXT"


commandNames = {"!100": command_hunad, "!afterstream": command_afterstream, "!crossplay": command_crossplay, "!debug": command_debug, "!discord": command_discord, "!donation": command_donation, "!filter": command_filter, "!godrays": command_godgays, "!konsole": command_konsole, "!lieblingswaffe": command_lieblingswaffe,
                "!listen": command_listen, "!michi": command_michi, "!reddit": command_reddit, "!roadto": command_roadto, "!sew": command_sew, "!spielstunden": command_spielstunden, "!statistik": command_statistik,  "!sub": command_sub, "!timemeout": command_timemeout, "!tlou": command_tlou, "!turnier": command_turnier, "!twitch": command_twitch, "!updateconsole": command_updateConsole, "!uptime": command_uptime, "!xp": command_xp}


def executeCommands(parentInputs):
    msgParts = parentInputs["message"]["snippet"]["textMessageDetails"]["messageText"].split(
        " ")
    print(msgParts)
    cmd = msgParts[0]
    if cmd in commandNames.keys():
        print(cmd)
        opt = {"isMod": parentInputs["message"]["authorDetails"]["isChatModerator"], "username": parentInputs["message"]["authorDetails"]["displayName"], "streamAge": parentInputs["streamAge"], "message": parentInputs["message"]
               ["snippet"]["textMessageDetails"]["messageText"], "strike": parentInputs["strike"], "userId": parentInputs["message"]["authorDetails"]["channelId"]}
        parentInputs["sendText"](
            commandNames[cmd](opt))
