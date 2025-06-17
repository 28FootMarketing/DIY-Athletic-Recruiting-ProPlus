def get_bot_response(user_data: dict) -> str:
    name = user_data.get("name", "Athlete")
    grade = user_data.get("current_grade_level", "")
    sport = user_data.get("primary_sport", "")
    motivation = user_data.get("motivation_level", "")
    outreach = user_data.get("outreach_status", "")

    response = [f"👋 Hey {name}! I'm Coach Khloe, your recruiting motivator. Let's break it down:"]

    if grade in ["9", "10"]:
        response.append("You’re in a great spot to build your foundation. Start collecting highlights, and build relationships early.")
    elif grade == "11":
        response.append("This is go-time! Junior year is critical—focus on outreach and exposure.")
    elif grade == "12" or "Post Grad":
        response.append("Every moment counts. Let’s make your profile undeniable and follow up with coaches weekly.")

    if motivation == "High":
        response.append("I love that energy! Channel it into weekly film reviews and email outreach.")
    elif motivation == "Medium":
        response.append("You’ve got a spark. Let's turn it into consistent action.")
    elif motivation == "Low":
        response.append("Even small steps count. Let's simplify things—just send one email this week.")

    if outreach == "No":
        response.append("Let’s fix that now. I’ll help you build your first outreach message.")
    elif outreach == "Some":
        response.append("Nice start. Now let’s get more strategic about follow-up.")
    elif outreach == "Yes, many":
        response.append("Great job! Let’s track who replied and build momentum.")

    response.append(f"\n📣 Your sport: {sport} — I’ve got drills, routines, and strategy tips queued up next!")

    return "\n".join(response)
