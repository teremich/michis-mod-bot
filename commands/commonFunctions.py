def sendText(youtube, CHATID, text, tag="NULL"):
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
    print(response)
