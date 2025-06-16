import json
import os

RANKED_MODULES_PATH = "data/ranked_modules.json"
TOGGLES_PATH = "data/module_toggles.json"

def validate_user_fields(user_data):
    required = ["name", "current_grade_level", "primary_sport", "gpa_score", "college_targets", "motivation_level", "outreach_status"]
    return [field for field in required if not user_data.get(field)]

def load_ranked_modules():
    if not os.path.exists(RANKED_MODULES_PATH):
        return []
    with open(RANKED_MODULES_PATH, "r") as f:
        return json.load(f)

def load_module_toggles():
    if not os.path.exists(TOGGLES_PATH):
        return {}
    with open(TOGGLES_PATH, "r") as f:
        return json.load(f)

def save_module_toggles(toggles):
    with open(TOGGLES_PATH, "w") as f:
        json.dump(toggles, f, indent=2)

def select_module_based_on_input(user_data):
    modules = load_ranked_modules()
    toggles = load_module_toggles()

    enabled_modules = [mod for mod in modules if toggles.get(str(mod["id"]), True)]

    if not enabled_modules:
        return None

    # Sample logic: prioritize by outreach level, then grade level, then module rank
    filtered = [
        mod for mod in enabled_modules
        if user_data["current_grade_level"] in mod.get("grades", []) or "All" in mod.get("grades", [])
    ]
    return filtered[0] if filtered else enabled_modules[0]
