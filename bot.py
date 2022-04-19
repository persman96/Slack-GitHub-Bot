import slack  # slackclient
import os
from pathlib import Path
from dotenv import load_dotenv  # python-dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from common import load_config_dict

app = Flask(__name__)

cfg = load_config_dict()
SIGNING_SECRET = cfg['signing_secret']
SLACK_TOKEN = cfg['slack_token']
API_PORT = cfg["api_port"]

# slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
# client = slack.WebClient(token=SLACK_TOKEN)
# BOT_ID = client.api_call("auth.test")['user_id']


# @slack_event_adapter.on('message')
# def message(payload):
#     event = payload.get('event', {})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')
#     if BOT_ID != user_id:
#         client.chat_postMessage(channel=channel_id, text=text)
#
#
# @app.route('/run-workflow', methods=['POST'])
# def run_workflow():
#     data = request.form
#     user_id = data.get('user_id')
#     channel_id = data.get('channel_id')
#
#     if BOT_ID != user_id:
#         client.chat_postMessage(channel=channel_id, text='Working on it!')
#
#     return Response(), 200


@app.route('/', methods=['POST'])
def handle_webhook(event):
    print(event)


if __name__ == "__main__":
    app.run(port=API_PORT, debug=True)
