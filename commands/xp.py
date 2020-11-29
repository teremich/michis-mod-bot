import urllib
import json
from commonFunctions import sendText


def xp(youtube, CHATID, msg):
    command = "!xp"
    res = urllib.request.urlopen(
        "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=326460&key=7359F5150A808259B6C38735D89B910A&steamid=76561198091960570")
    jsonRes = json.loads(res)
    xp = ""
    for item in jsonRes["playerstats"]["achievements"]:
        if item["name"] == "xp":
            xp = item["value"]
    if command == msg["snippet"]["textMessageDetails"]["messageText"][:len(command)]:
        sendText(
            youtube, CHATID, xp, msg["authorDetails"]["displayName"])
