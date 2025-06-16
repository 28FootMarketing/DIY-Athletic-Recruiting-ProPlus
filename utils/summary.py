def build_summary(user_data, module_name):
    name = user_data.get("name", "Athlete")
    sport = user_data.get("primary_sport", "your sport")
    grade = user_data.get("current_grade_level", "N/A")

    summary = f"""
Hey {name}, based on your current status as a {grade} grade {sport} athlete, your next recommended step is to dive into the "{module_name}" module.

This will help you stay focused, organized, and ready for the next level. Keep showing up and putting in the work. You do not have to be perfect — just prepared.

Let’s keep building. 💪🏽🏅
"""
    return summary.strip()
