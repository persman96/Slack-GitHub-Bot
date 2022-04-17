import toml
import logging

cfg_path = "config.toml"


def load_config_dict() -> dict:
    """
    Loads the config file and returns a dictionary with the config.
    """
    try:
        with open(cfg_path) as cfg:
            return toml.load(cfg, _dict=dict)
    except FileNotFoundError:
        logging.error("Config file not found")
