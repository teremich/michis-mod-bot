import os
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from commands import *

# This should be 'False', pls fix, if I uploaded it incorrectly
TESTRUN = True

# Commands
commandsList = [
    xp
]


# Get credentials and create an API client
scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = os.path.dirname(
    os.path.abspath(__file__))+"\\client_secret.json"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
if not TESTRUN:
    credentials = flow.run_console()
else:
    credentials = flow.run_local_server()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


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


def main():
    while True:
        # Searching for Livestream by User with below written channelId

        request = youtube.search().list(
            part="snippet",
            channelId="UCvlsCHPqjj4Ydanpp_QZeOA",
            eventType="live",
            maxResults=1,
            type="video"
        )
        hour = int(time.strftime("%H", time.localtime()))
        if hour > 14 and hour < 22 or TESTRUN:
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

                    def listenForWords(message):
                        # Define words to listen for and the responses to give
                        activatorWords = getListen()
                        for activator in activatorWords:
                            if (activator["word"] in message["snippet"]["textMessageDetails"]["messageText"]):
                                sendText(activator["response"],
                                         message["authorDetails"]["displayName"])

                    def listenForCommands(message):
                        for com in commandsList:
                            com({"sendText": sendText}, message)

                    i = 0
                    for i in range(len(response["items"])-1, -1, -1):
                        if response["items"][i]["id"] == newestChatId:
                            break
                    for j in range(i, len(response["items"])):
                        message = response["items"][j]
                        # listenForSpam(message)
                        # listenForFilter(message)
                        listenForWords(message)
                        listenForCommands(message)

                    newestChatId = response["items"][-1]["id"]
                except IndexError:
                    break


if __name__ == "__main__":
    main()
