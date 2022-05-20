# michis mod bot

This is a youtube livestream moderation bot specifically designed for "Der Michi" (youtube.com/channel/UCGDTo1icA1LW56wWGIQ9GQA).

What to install:

-   python 3.8.5 (this version is tested but preferable is the newest version)
-   pip
    -   best practice is to install packages in a virtual environment
    -   pip install --upgrade google-api-python-client
    -   pip install --upgrade google-auth-oauthlib google-auth-httplib2

Things to do if you want to copy the code:

-   Make a Youtube account for the bot, give it mod rights.
-   Get 2 API client secret files from google (console.developers.google.com)
-   name one "client_secret.json" and the other one "stream_client_secret.json"
-   change the User ID in app.py to the streamers Youtube ID

start with "python app.py"
At start choose to log in via the bot's account.

