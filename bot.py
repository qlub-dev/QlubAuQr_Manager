import os
import slack
from flask import Flask
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from bot_util import upload_or_update

load_dotenv()


app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.getenv("SIGNING_SECRET"), "/slack/events", app
)
slack_client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))
BOT_ID = slack_client.api_call("auth.test")["user_id"]


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    command = text.split()[0]

    if BOT_ID != user_id:
        if command in ["upload", "update"]:
            upload_or_update(slack_client=slack_client, event=event)
        slack_client.chat_postMessage(
            channel=channel_id, text="Hi there I'm Lila your upload/update assistant"
        )


if __name__ == "__main__":
    app.run(debug=True)
