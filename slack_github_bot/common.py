import os
import pathlib
import toml
from logging import error

current_dir = pathlib.Path(__file__).parent.absolute()
CFG_PATH = os.path.join(current_dir, "config.toml")


def load_config_dict() -> dict:
    """
    Loads the config file and returns a dictionary with the config.
    """
    try:
        with open(CFG_PATH, "r") as cfg:
            return toml.load(cfg, _dict=dict)
    except FileNotFoundError:
        error("Config file not found")
        return None


def parse_workflow_run(run: dict) -> dict:
    """
    Parses a workflow run to extract relevant information.
    """
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
