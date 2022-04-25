## Slack-GitHub-Bot

Simple costum slack Github bot to interact with Github Actions.

### Installation

```bash 
git clone git@github.com:persman96/Slack-GitHub-Bot.git
cd Slack-GitHub-Bot
pip3 install .
```

 ### Configuration

#### Slack
To start, you need to register a slack bot on the Slack website (Setup Slack bot: https://api.slack.com/apps).
This allows you to get a slack token and a signing key, which we set as environment variables.

```bash
export signing_key=<your signing key>
export slack_token=<your slack token>
```

#### Github
You need to create a token on Github with the permissions to trigger Github Actions.
Additonally, you have to setup a webhook on your Github repository. 
Go to settings -> webhooks -> add webhook, choose "application/json" and set the url to the url of the bot server ip.

```bash
export github_token=<your github token>
export github_repo=<your github repository>
```

#### Hosting

It makes the most sense to deploy this bot to get a fixed endpoint address. For testing purposes you can use a service like ngrok which creates a tunnel to the local machine.


### Start
To start the bot you should execute the following command:
```bash
python3 slack_github_bot/api.py
```

### Usage 

After the Github bot is added to the Slack workspace, you can chat with it.
To execute a command start with a "/" backslash and then you already get suggestions for possible commands

Currently implemented are: 
* /run-workflow
* /get_branches
* /get_all_workflows
* /get_all_workflow_runs
* /get_workflow_run
* /create_workflow_dispatch_event
* /meme


