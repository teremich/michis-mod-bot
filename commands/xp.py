import urllib
import json


def xp(parentInputs, msg):
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
