import json
import random
import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from slack_github_bot.common import load_config_dict, parse_workflow_run
from slack_github_bot.api import *
import os

app = Flask(__name__)
"""
cfg = load_config_dict()

SIGNING_SECRET = cfg['signing_secret']
SLACK_TOKEN = cfg['slack_token']
API_PORT = cfg["api_port"]
"""

SIGNING_SECRET = os.environ['signing_secret']
SLACK_TOKEN = os.environ['slack_token']
API_PORT = os.environ["api_port"]

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


@app.route('/get_branches', methods=['POST'])
def get_branches():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    branches = get_branches_of_repo()
    response = [f"{branch} \t" for branch in branches]
    list = []
    for branch in branches:
        section = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": branch
            }
        }
        list.append(section)

    # block = {"blocks": list}
    # b = json.dumps(block)

    if response and BOT_ID != user_id:
        # client.chat_postMessage(channel=channel_id, text=b)
        client.chat_postMessage(channel=channel_id, blocks=list, text=branches)

    return Response(), 200


@app.route('/get_all_workflows', methods=['POST'])
def workflow_of_repo():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    response = ""
    workflows = get_all_workflows_of_repo()

    for workflow in workflows["workflows"]:
        name = workflow["name"]
        file_name = workflow["path"].split("/")[-1]
        url = workflow["html_url"]

        response += f"Name: {name} \t File: {file_name} \t {url}\n"

    if response and BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=response)

    return Response(), 200


@app.route('/get_all_workflows_runs', methods=['POST'])
def workflow_runs_of_repo():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    response = ""
    workflow_runs = get_workflow_runs_of_repo()

    text = data.get("text")
    text_arr = text.split(" ")
    if len(text_arr) > 1 and 0 < int(text_arr[1]) <= len(workflow_runs):
        n = int(text_arr[1])
    else:
        n = len(workflow_runs)

    for run in workflow_runs[:n]:
        name = run["name"]
        branch = run["head_branch"]
        user = run["trigger_user"]
        conclusion = run["conclusion"]
        status = run["status"]
        created_at = run["created_at"]

        response += f"Name: {name} \t Branch: {branch} \t User: {user} \t Conclusion: {conclusion} \t Status: {status} Created at: {created_at}\n"

    if response and BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=response)

    return Response(), 200


# Example id from our repo: 2197509667
@app.route('/get_workflow_run', methods=['POST'])
def workflow_run():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    run_id = int(data.get('text'))

    response = get_workflow_run(run_id)

    if response and BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=response)

    return Response(), 200


@app.route('/create_workflow_dispatch_event', methods=['POST'])
def workflow_dispatch_event():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    run_ID = text.split(' ')[0]
    branch = text.split(' ')[1]

    success = create_workflow_dispatch_event(run_ID, branch)

    if success:
        response = f"Workflow {run_ID} dispatched on branch {branch}!"
    else:
        response = f"Workflow {run_ID} could not be dispatched on branch {branch}!"

    if response and BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=response)

    return Response(), 200


@app.route('/meme', methods=['POST'])
def show_meme():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    # get directory of file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'memes.txt'), 'r') as f:
        meme_urls = f.read().splitlines()
    meme_url = random.choice(meme_urls)

    # create block to display meme
    block = {
        "blocks": [
            {
                "type": "image",
                "image_url": meme_url,
                "alt_text": "meme"
            }
        ]
    }
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, blocks=block)

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
        if conclusion:
            response = f"Workflow {name} on branch {branch}: {conclusion}"
            channel_id = "C03BV0JMXQC"
            client.chat_postMessage(channel=channel_id, text=response)

    return Response(), 200


if __name__ == "__main__":
    app.run(port=API_PORT, debug=True)
