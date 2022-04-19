import json
import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from slack_github_bot.common import load_config_dict, parse_workflow_run

app = Flask(__name__)

cfg = load_config_dict()
SIGNING_SECRET = cfg['signing_secret']
SLACK_TOKEN = cfg['slack_token']
API_PORT = cfg["api_port"]

slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)
client = slack.WebClient(token=SLACK_TOKEN)
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


@app.route('/', methods=['POST'])
def handle_webhook():
    """
    Endpoint to receive webhooks from GitHub API.
    Currently, only handles workflow_run events.
    """
    payload = request.get_data().decode('utf-8')
    data_dict = json.loads(payload)

    # with open(f'tmp/payload-{counter}.json', 'w') as f:
    #     json.dump(data_dict, f)

    workflow_data = data_dict.get("workflow_run", False)
    if workflow_data:
        run = parse_workflow_run(data_dict["workflow_run"])
        name, branch, conclusion = run["name"], run["head_branch"], run["conclusion"]
        print(f"Workflow {name} on branch {branch}: {conclusion}")
        # TODO send message to slack channel

    return Response(), 200


if __name__ == "__main__":
    app.run(port=API_PORT, debug=True)
