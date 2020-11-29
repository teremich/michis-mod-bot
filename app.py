import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from commands import commonFunctions
from commands import xp

# Define commands
commandsList = [
    xp.xp
]

# Define words to listen for
activatorWords = [
    {
        "word": "mitspielen",
        "response": "Mitspielen kann jeder, egal welches Level. Ihr müsst nur die Lobby finden und dieser joinen."
    },
    {
        "word": "mitmachen",
        "response": "Mitspielen kann jeder, egal welches Level. Ihr müsst nur die Lobby finden und dieser joinen."
    }
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
credentials = flow.run_local_server()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

# Searching for Livestream by User with below written channelId
request = youtube.search().list(
    part="snippet",
    channelId="UCvlsCHPqjj4Ydanpp_QZeOA",
    eventType="live",
    maxResults=1,
    type="video"
)
response = request.execute()
vidid = ""
# Getting the VideoId or raising error if no livestream was found
try:
    vidid = response["items"][0]["id"]["videoId"]
except IndexError:
    raise Exception("NO LIVESTREAMS FOR THAT USER")

# Getting id for the chat of the livestream
request = youtube.videos().list(
    part="snippet,contentDetails,statistics,liveStreamingDetails",
    id=vidid
)
response = request.execute()

CHATID = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
print(CHATID)
# Getting 2000 messages from youtube
request = youtube.liveChatMessages().list(
    liveChatId=CHATID,
    part="id,snippet,authorDetails",
    maxResults=2000
)
response = request.execute()


# printing the message texts.
msgs = response["items"]
msgs = msgs[::-1]
for message in msgs:
    for activator in activatorWords:
        if (activator["word"] in message["snippet"]["textMessageDetails"]["messageText"]):
            commonFunctions.sendText(youtube, CHATID, activator["response"],
                                     message["authorDetails"]["displayName"])
    for com in commandsList:
        com(youtube, CHATID, message)
