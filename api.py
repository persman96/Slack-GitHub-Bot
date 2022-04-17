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
        branches = response.json()
        return branches
    except Exception as e:
        error(f"Error: {e}")
        return None


def get_artifacts(branch: str = "main") -> Optional[list]:
    """
    Get all artifacts from a repository.2
    :param branch: optional, the branch to get artifacts from
    :return: list with all artifacts
    """
    ENDPOINT = f" https://api.github.com/repos/{owner}/{repo}/actions/artifacts"
    try:
        response = get(ENDPOINT, headers={"Authorization": f"token {token}"}, data={"ref": branch}, timeout=timeout)
        artifacts = response.json()
        return artifacts
    except Exception as e:
        error(f"Error: {e}")
        return None


def get_action_permissions_of_repo() -> Optional[dict]:
    """
    Get all action permissions of a repository.
    :return: dict with all action permissions
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/permissions"
    try:
        response = get(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        permissions = response.json()
        return permissions
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
        workflows = response.json()
        return workflows
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
        runs = response.json()
        return runs
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
        return run
    except Exception as e:
        error(f"Error: {e}")
        return None


def disable_workflow(workflow_id: int) -> bool:
    """
    Disable a workflow.
    :param: bool, True if successful, False if not
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/disable"
    try:
        response = post(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        return response.status_code == 204
    except Exception as e:
        error(f"Error: {e}")
        return False


def enable_workflow(workflow_id: int) -> bool:
    """
    Enable a workflow.
    :param: bool, True if successful, False if not
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/enable"
    try:
        response = post(ENDPOINT, headers={"Authorization": f"token {token}"}, timeout=timeout)
        return response.status_code == 204
    except Exception as e:
        error(f"Error: {e}")
        return False


def create_workflow_dispatch_event(workflow_id: str, ref: str = "main", inputs: dict = {}) -> bool:
    """
    Function to manually trigger a GitHub Actions workflow run
    :param workflow_id: str, name of the workflow e.g. "main.yaml"
    :param ref: str, name of the branch or tag to trigger the workflow on
    :param inputs: dict, optional, inputs for the workflow
    :return: bool, True if successfully triggered pipeline, False if not
    """
    ENDPOINT = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
    try:
        response = post(ENDPOINT, headers={"Authorization": f"token {token}"}, data={"inputs": str(inputs), "ref": ref}, timeout=timeout)
        return response.status_code == 204
    except Exception as e:
        error(f"Error: {e}")
        return False