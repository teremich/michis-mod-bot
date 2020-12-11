import os
import time
import math
import datetime

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from commands import executeCommands

# This should be 'False', pls fix, if I uploaded it incorrectly
TESTRUN = False

# Get credentials and create an API client
scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = os.path.dirname(
    os.path.abspath(__file__))+"\\client_secret.json"
stream_client_secrets_file = os.path.dirname(
    os.path.abspath(__file__))+"\\stream_client_secret.json"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
stream_flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    stream_client_secrets_file, scopes)
if not TESTRUN:
    credentials = flow.run_console()
else:
    credentials = flow.run_local_server()
stream_credentials = stream_flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
stream_youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=stream_credentials)


def getListen():
    toRet = {}
    with open("listen.txt", "r", encoding="utf-8") as f:
        for line in f:
            splitter = line.find(":")
            if line[-1] == "\n":
                toRet[line[:splitter]] = line[splitter+1:-1]
            else:
                toRet[line[:splitter]] = line[splitter+1:]
    return toRet


def getFilter():
    words = []
    with open("filter.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line == "\n":
                continue
            if line[-1] == "\n":
                words.append(line[:-1].lower())
            else:
                words.append(line.lower())

    return words


def count(item, L):
    c = 0
    for o in L:
        if o == item:
            c += 1
    return c


def rndFromList(L):
    max = len(L)
    range = math.random()*max
    index = math.floor(range)
    return L[index]


def main():
    while True:
        # Searching for Livestream by User with below written channelId

        request = stream_youtube.search().list(
            part="snippet",
            channelId="UCGDTo1icA1LW56wWGIQ9GQA",
            eventType="live",
            maxResults=1,
            type="video"
        )
        hour = int(time.strftime("%H", time.localtime()))
        if hour > 14 and hour < 23 or TESTRUN:
            try:
                response = request.execute()
                if TESTRUN:
                    print("searching for stream...")
                    print(response)
            except Exception:
                print("no more power to search for a stream using other method")
                if TESTRUN:
                    response = {
                        "items": [
                            {
                                "id": {
                                    "videoId": input("pls give me a vidid")
                                }
                            }
                        ]
                    }
        else:
            response = {"items": []}
        if TESTRUN:
            print(hour)
        vidid = ""
        # Getting the VideoId or raising error if no livestream was found
        try:
            vidid = response["items"][0]["id"]["videoId"]
        except IndexError:
            print("No Livestream active")
            time.sleep(60*5)
        else:
            # Getting id for the chat of the livestream
            request = stream_youtube.videos().list(
                part="snippet,contentDetails,statistics,liveStreamingDetails",
                id=vidid
            )
            response = request.execute()
            if len(response["items"]) < 1:
                continue
            CHATID = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
            STREAMAGE = response["items"][0]["snippet"]["publishedAt"]
            STREAMAGE = datetime.datetime.strptime(
                STREAMAGE, "%Y-%m-%dT%H:%M:%SZ")
            print(STREAMAGE, type(STREAMAGE))
            print(CHATID)
            strikes = {}
            activatorWords = getListen()
            wordFilter = getFilter()
            request = stream_youtube.liveChatMessages().list(
                liveChatId=CHATID,
                part="id,snippet,authorDetails",
                maxResults=2000
            )
            response = request.execute()
            newestChatId = response["items"][-1]["id"]
            while True:
                try:
                    # Getting 2000 messages from youtube
                    request = youtube.liveChatMessages().list(
                        liveChatId=CHATID,
                        part="id,snippet,authorDetails",
                        maxResults=2000
                    )
                    response = request.execute()
                    if "error" in response.keys():
                        print("Could not read Chat Messages, trying to reconnect...")
                        raise IndexError(
                            "Could not read Chat Messages, trying to reconnect...")
                    if TESTRUN:
                        print("only defs after here")

                    def sendText(text, tag="NULL"):
                        if tag == "NULL":
                            msgText = str(text)[:200]
                        else:
                            msgText = "@{0} -> {1}".format(tag, text)[:200]
                        request = youtube.liveChatMessages().insert(
                            part="snippet",
                            body={
                                "snippet": {
                                    "liveChatId": CHATID,
                                    "type": "textMessageEvent",
                                    "textMessageDetails": {
                                            "messageText": msgText
                                    }
                                }
                            }
                        )
                        response = request.execute()
                        if TESTRUN:
                            print(response)
                        if "error" in response.keys():
                            print(
                                "Could not write a message to Chat, trying to reconnect...")
                            raise IndexError(
                                "Could not write a message to Chat, trying to reconnect...")
                        return response["id"]

                    def sendTimeout(channelId, duration):
                        try:
                            print(
                                "sent timeout request with following parameters:", channelId, duration)
                            request = youtube.liveChatBans().insert(
                                part="snippet",
                                body={
                                    "snippet": {
                                        "type": "temporary",
                                        "bannedUserDetails": {
                                                "channelId": channelId
                                        },
                                        "liveChatId": CHATID,
                                        "banDurationSeconds": duration
                                    }
                                }
                            )
                            response = request.execute()
                            print(response)
                        except Exception:
                            newestChatId = sendText(
                                "Ich hätte dir schon nen Timeout gegeben, wenn ich könnte")
                            print("didnt work, probably mod or streamer")

                    def listenForWords(message):
                        # Define words to listen for and the responses to give
                        for word in activatorWords:
                            if (word in message["snippet"]["textMessageDetails"]["messageText"].lower()):
                                newestChatId = sendText(activatorWords[word],
                                                        message["authorDetails"]["displayName"])

                    def strike(userid):
                        if userid in strikes.keys():
                            strikes[userid]["count"] += 1
                        else:
                            strikes[userid] = {
                                "count": 1, "made": time.time()}
                        strength = strikes[userid]["count"]
                        if strength == 1:
                            duration = 5
                        elif strength == 2:
                            duration = 20
                        else:
                            duration = 300
                        sendTimeout(userid, duration)

                    def listenForCaps(message):
                        msg = message["snippet"]["textMessageDetails"]["messageText"]
                        if (msg == msg.upper() and len(msg) > 5):
                            strike(message["authorDetails"]["channelId"])
                            answers = [
                                "AHHH! CAPS", "bitte kein caps :(", "nein nein nein! böses caps!"]
                            newestChatId = sendText(rndFromList(answers),
                                                    message["authorDetails"]["displayName"])

                    def listenForFilter(message):
                        messageWords = message["snippet"]["textMessageDetails"]["messageText"].split(
                            " ")

                        for word in messageWords:
                            if TESTRUN:
                                print(word)
                            if word.lower() in wordFilter:
                                if TESTRUN:
                                    print("FOUND BAD WORD")
                                userid = message["authorDetails"]["channelId"]
                                strike(userid)
                                answers = ["Kannst du das nochmal ohne '"+word +
                                           "' sagen?", "Wir sprechen nicht mehr über "+word, ]
                                newestChatId = sendText(rndFromList(answers),
                                                        message["authorDetails"]["displayName"])

                    def listenForSpam(items):
                        users = []
                        for msgRes in items:
                            for userObj in users:
                                if userObj["id"] == msgRes["authorDetails"]["channelId"]:
                                    userObj["msgs"].append(
                                        msgRes["snippet"]["textMessageDetails"]["messageText"])
                            else:
                                users.append({"id": msgRes["authorDetails"]["channelId"], "msgs": [
                                    msgRes["snippet"]["textMessageDetails"]["messageText"]]})
                        for user in users:
                            for msg in user["msgs"]:
                                if count(msg, user["msgs"]) > 3:
                                    strike(user["id"])
                    if TESTRUN:
                        print("the rest should work fine")
                    for s in strikes:
                        if strikes[s]["made"] < time.time()-30*60:
                            del strikes[s]

                    i = 0
                    for i in range(len(response["items"])-1, -1, -1):
                        if response["items"][i]["id"] == newestChatId:
                            i += 1
                            break
                    if i < len(response["items"]):
                        listenForSpam(response["items"])
                        newestChatId = response["items"][-1]["id"]
                        for j in range(i, len(response["items"])):
                            message = response["items"][j]
                            listenForCaps(message)
                            listenForFilter(message)
                            listenForWords(message)
                            executeCommands(
                                {"sendText": sendText, "streamAge": STREAMAGE, "message": message})

                    if TESTRUN:
                        print("finished at least once")
                    time.sleep(5)
                except (IndexError, Exception):
                    break


if __name__ == "__main__":
    main()
