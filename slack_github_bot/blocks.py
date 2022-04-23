from slack_github_bot.api import *

def create_dispatch_block():
    workflows = get_workflows()
    options_workflow = []
    for workflow in workflows['workflows']:
        wf_name = workflow['name']
        path = workflow['path']
        file_name = path.split("/")[-1]
        options_workflow.append({"text": {
            "type": "plain_text",
            "text": wf_name
        },
            "value": file_name
        })

    branches = get_branches_of_repo()
    options_branches = []
    for branch in branches:
        options_branches.append({"text": {
            "type": "plain_text",
            "text": branch
        },
            "value": branch
        })

    workflow_field = {
        "type": "static_select",
        "placeholder": {
            "type": "plain_text",
            "text": "Select a workflow",
        },
        "options": options_workflow,
        "action_id": "workflows"
    }
    branch_field = {
        "type": "static_select",
        "placeholder": {
            "type": "plain_text",
            "text": "Select a branch",
        },
        "options": options_branches,
        "action_id": "branches"
    }
    elements = [workflow_field, branch_field]
    block = [{
			"type": "section",
			"block_id": "section678",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a workflow and a branch from the dropdown list!"
			        }
            },
            {"type": "actions",
                  "block_id": "create_dispatch",
                  "elements": elements
                  }]
    return block


def parse_dispatch_response(response):

    try:
        selected_option = response['state']['values']['create_dispatch']['workflows']['selected_option']
        if selected_option != None:
            workflow = selected_option['value']
        else:
            workflow = ""
    except:
        workflow = ""
        print("could not read workflow")

    try:
        selected_option = response['state']['values']['create_dispatch']['branches']['selected_option']
        if selected_option != None:
            branch = selected_option['value']
        else:
            branch = ""
    except:
        branch = ""
        print("could not read branch")

    return workflow, branch

