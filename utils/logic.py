def validate_user_fields(user_data):
    required_fields = ["current_grade_level", "primary_sport", "college_targets", "motivation_level", "outreach_status", "gpa_score"]
    missing = [field for field in required_fields if field not in user_data or not user_data[field]]
    return missing

def select_module_based_on_input(user_data):
    grade = user_data.get("current_grade_level")
    motivation = user_data.get("motivation_level")

    if grade in ["9", "10"]:
        return "Recruiting Profile Builder"
    elif grade == "11":
        return "Target School Generator"
    elif grade == "12" and motivation.lower() == "high":
        return "Coach Messaging & Follow-Up System"
    else:
        return "Mental Performance & Confidence Coach"

