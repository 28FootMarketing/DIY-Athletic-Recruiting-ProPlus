import json
import os

CONFIG_FILE = "module_config.json"

def load_module_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_module_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
