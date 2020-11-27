import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Get credentials and create an API client
scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
	client_secrets_file, scopes)
credentials = flow.run_local_server()
youtube = googleapiclient.discovery.build(
	api_service_name, api_version, credentials=credentials)


request = youtube.search().list(
	part="snippet",
	channelId="UCGDTo1icA1LW56wWGIQ9GQA",
	eventType="live",
	maxResults=1,
	type="video"
)
response = request.execute()
vidid = ""

try:
	vidid = response["items"][0]["id"]["videoId"]
except IndexError:
	raise Exception("NO LIVESTREAMS FOR THAT USER (Der Michi)")

request = youtube.videos().list(
	part="snippet,contentDetails,statistics,liveStreamingDetails",
	id=vidid
)
response = request.execute()

CHATID = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]