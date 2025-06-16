import json
import os

# Load the ranked modules list from JSON
MODULES_PATH = os.path.join(os.path.dirname(__file__), "../data/ranked_modules.json")

def load_ranked_modules():
    with open(MODULES_PATH, "r") as f:
        return json.load(f)

def validate_user_fields(user_data):
    required_fields = ["name", "current_grade_level", "primary_sport", "gpa_score", "college_targets", "motivation_level", "outreach_status"]
    missing = [field for field in required_fields if not user_data.get(field)]
    return missing

def select_module_based_on_input(user_data):
    modules = load_ranked_modules()
    grade = user_data.get("current_grade_level")
    outreach = user_data.get("outreach_status")

    if grade == "9":
        return modules[0]["name"]  # Recruiting Profile Builder
    elif grade in ["10", "11"] and outreach == "No":
        return modules[2]["name"]  # Target School Generator
    elif grade in ["11", "12"] and outreach == "Some":
        return modules[6]["name"]  # Highlight Video & Content Strategy
    elif grade == "Post Grad":
        return modules[14]["name"]  # Post-Graduate & JUCO Route Planner
    else:
        return modules[9]["name"]  # Recruiting Timeline & Task Tracker
