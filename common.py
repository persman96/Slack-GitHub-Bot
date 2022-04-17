from logging import error
import toml

CFG_PATH = "config.toml"


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
