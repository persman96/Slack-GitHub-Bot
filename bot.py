import slack # slackclient
import os
from pathlib import Path
from dotenv import load_dotenv # python-dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

@app.route('/run-workflow', methods=['POST'])
def run_workflow():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text='Working on it!')

    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)
