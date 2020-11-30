import os
import time

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
    with open("listen.txt", "r+") as f:
        for line in f:
            if line[-1] == "\n":
                excludeNewLine = 1
            else:
                excludeNewLine = 0
            splitter = line.find(":")
            toRet[line[:splitter]] = line[splitter+1:-excludeNewLine]
    return toRet


def count(item, L):
    c = 0
    for o in L:
        if o == item:
            c += 1
    return c


def main():
    while True:
        # Searching for Livestream by User with below written channelId

        request = stream_youtube.search().list(
            part="snippet",
            channelId="UCvlsCHPqjj4Ydanpp_QZeOA",
            eventType="live",
            maxResults=1,
            type="video"
        )
        hour = int(time.strftime("%H", time.localtime()))
        if hour > 15 and hour < 23 or TESTRUN:
            response = request.execute()
        else:
            response = {"items": []}
        vidid = ""
        # Getting the VideoId or raising error if no livestream was found
        try:
            vidid = response["items"][0]["id"]["videoId"]
        except IndexError:
            print("No Livestream active")
            time.sleep(60*5)
        else:
            # Getting id for the chat of the livestream
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics,liveStreamingDetails",
                id=vidid
            )
            response = request.execute()
            if len(response["items"]) < 1:
                continue
            CHATID = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
            print(CHATID)
            newestChatId = ""
            strikes = {}
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
                        raise IndexError(
                            "Could not read Chat Messages, trying to reconnect...")

                    def sendText(text, tag="NULL"):
                        if tag == "NULL":
                            msgText = text[:200]
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
                            raise IndexError(
                                "Could not write a message to Chat, trying to reconnect...")

                    def sendTimeout(channelId, duration):
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

                    def listenForWords(message):
                        # Define words to listen for and the responses to give
                        activatorWords = getListen()
                        for word in activatorWords:
                            if (word in message["snippet"]["textMessageDetails"]["messageText"]):
                                sendText(activatorWords[word],
                                         message["authorDetails"]["displayName"])

                    def strike(userid, strength):
                        if strength == 1:
                            duration = 5
                        elif strength == 2:
                            duration = 20
                        else:
                            duration = 300
                        sendTimeout(userid, duration)

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
                                    if user["id"] in strikes.keys():
                                        strikes[user["id"]]["count"] += 1
                                    else:
                                        strikes[user["id"]] = {
                                            "count": 1, "made": time.time()}
                                    strike(
                                        user["id"], strikes[user["id"]]["count"])
                        for s in strikes:
                            if strikes[s]["made"] < time.time()-30*60:
                                del strikes[s]

                    i = 0
                    for i in range(len(response["items"])-1, -1, -1):
                        if response["items"][i]["id"] == newestChatId:
                            i += 1
                            break
                    listenForSpam(response["items"])
                    for j in range(i, len(response["items"])):
                        message = response["items"][j]
                        # listenForFilter(message)
                        listenForWords(message)
                        executeCommands({"sendText": sendText}, message)

                    newestChatId = response["items"][-1]["id"]
                except IndexError:
                    break


if __name__ == "__main__":
    main()
