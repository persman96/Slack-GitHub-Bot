import json
from typing import Optional
from requests import get, post
from common import load_config_dict
from logging import info, error, debug

config = load_config_dict()

owner = config["repository_link"].split("/")[-2]
repo = config["repository_link"].split("/")[-1]
token = config["authorization_token"]
timeout = config["timeout"]


def get_branches_of_repo() -> Optional[list]:
    """
    Get all branches of a repository.
    :return:
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/branches"
    try:
        response = get(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        return [branch["name"] for branch in response.json()]
    except Exception as e:
        error(f"Error: {e}")
        return None


def get_all_workflows_of_repo() -> Optional[list]:
    """
    Get all workflows of a repository.
    :return: list with all workflows
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
    try:
        response = get(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        return response.json()
    except Exception as e:
        error(f"Error: {e}")
        return None


def get_workflow_runs_of_repo() -> Optional[list]:
    """
    Get all workflow runs of a repository.
    :return: list with all workflow runs
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    try:
        response = get(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        workflow_runs = response.json()["workflow_runs"]
        # extract only relevant information
        return [{
            "id": run["id"],
            "name": run["name"],
            "head_branch": run["head_branch"],
            "head_sha": run["head_sha"],
            "conclusion": run["conclusion"],
            "status": run["status"],
            "created_at": run["created_at"],
            "updated_at": run["updated_at"],
            "trigger_user": run["triggering_actor"]["login"],
        } for run in workflow_runs]
    except Exception as e:
        error(f"Error: {e}")
        return None


def get_workflow_run(run_id: int) -> Optional[dict]:
    """
    Get a workflow run.
    :return: dict with specific workflow run
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"
    try:
        response = get(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        run = response.json()
        return {
            "id": run["id"],
            "name": run["name"],
            "head_branch": run["head_branch"],
            "head_sha": run["head_sha"],
            "conclusion": run["conclusion"],
            "status": run["status"],
            "created_at": run["created_at"],
            "updated_at": run["updated_at"],
            "trigger_user": run["triggering_actor"]["login"],
        }
    except Exception as e:
        error(f"Error: {e}")
        return None


def create_workflow_dispatch_event(workflow_id: str, branch: str = "main") -> bool:
    """
    Function to manually trigger a GitHub Actions workflow run
    :param workflow_id:  name of the workflow e.g. "main.yaml"
    :param branch  name of the branch or tag to trigger the workflow on
    :return: True if successfully triggered pipeline, False if not
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    try:
        response = post(ENDPOINT,
                        headers={"Accept": "application/vnd.github.everest-preview+json",
                                 "Authorization": f"token {token}"},
                        data=json.dumps({"ref": branch}),
                        timeout=timeout)
        return response.status_code == 204
    except Exception as e:
        error(f"Error: {e}")
        return False



