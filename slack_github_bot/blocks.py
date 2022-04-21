from slack_github_bot.api import *

def create_dispatch_block():
    workflows = get_workflows()
    options_workflow = []
    for workflow in workflows['workflows']:
        wf_name = workflow['name']
        options_workflow.append({"text": {
            "type": "plain_text",
            "text": wf_name
        },
            "value": wf_name
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
        "action_id": workflows
    }
    branch_field = {
        "type": "static_select",
        "placeholder": {
            "type": "plain_text",
            "text": "Select a branch",
        },
        "options": options_branches,
        "action_id": branches
    }
    elements = [workflow_field, branch_field]
    block = [{"type": "actions",
              "elements": elements
              }]
    return block

def parse_dispatch_response(response):
    block_id = response['actions'][0]['block_id']
    workflow = response['state']['values'][block_id]['workflows']['selected_option']['text']['text']
    branch = response['state']['values'][block_id]['branches']['selected_option']['text']['text']
    return workflow, branch

