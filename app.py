
import streamlit as st
import os
from dotenv import load_dotenv
from utils.logic_admin import (
    validate_user_fields,
    select_module_based_on_input,
    load_module_toggles,
    save_module_toggles,
    load_ranked_modules
)
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ Streamlit Page Config
st.set_page_config(page_title="DIY Recruiting-ProPlus", layout="wide")

# ✅ Load environment variables
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# ✅ Load Custom Styling
if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Sidebar: Admin Login + Roadmap
st.sidebar.title("Navigation")
tab_selection = st.sidebar.radio("Go to:", ["Recruiting Assistant", "Roadmap", "Admin Panel"])

# 🔐 Admin Login
st.sidebar.markdown("## Admin Access")
admin_input = st.sidebar.text_input("Enter admin password", type="password")
is_admin = (admin_input == ADMIN_PASSWORD)

# 🔁 Admin Module Toggle Panel
if tab_selection == "Admin Panel":
    st.header("🔐 Admin Module Manager")
    if is_admin:
        st.success("Access granted. Manage modules below.")
        toggles = load_module_toggles()
        updated = False
        for mod in load_ranked_modules():
            label = f"{mod['id']}. {mod['name']}"
            current = toggles.get(str(mod["id"]), True)
            new = st.checkbox(label, value=current)
            if new != current:
                toggles[str(mod["id"])] = new
                updated = True
        if updated:
            save_module_toggles(toggles)
            st.success("✅ Module toggles updated.")
    else:
        st.warning("Admin access required to manage modules.")

# 📅 Roadmap Tab
elif tab_selection == "Roadmap":
    st.header("📅 Recruiting-ProPlus Roadmap")
    st.markdown("Here is a look at upcoming features and releases.")
    roadmap = {
        "July": ["Interactive GPA Tracker", "Advanced Coach Messaging Templates"],
        "August": ["NIL Module Enhancements", "Mobile Optimization"],
        "September": ["AI Skill Evaluator", "Highlight Video Analyzer"]
    }
    for month, features in roadmap.items():
        st.markdown(f"### {month}")
        for item in features:
            st.markdown(f"- {item}")

# 🧠 Recruiting Assistant Main Interface
else:
    st.title("🏅 DIY Athletic Recruiting-ProPlus")
    st.subheader("Your step-by-step recruiting assistant")
    st.markdown("Stay focused, stay ready. Let’s keep building. 💪🏽")

    with st.form("user_input_form"):
        st.write("### Athlete Info")
        name = st.text_input("Full Name")
        current_grade_level = st.selectbox("Grade Level", ["9", "10", "11", "12", "Post Grad"])
        primary_sport = st.selectbox("Primary Sport", ["Football", "Basketball", "Baseball", "Softball", "Soccer", "Track", "Wrestling", "Volleyball", "Esports", "Other"])
        gpa_score = st.text_input("Current GPA")
        college_targets = st.text_input("List target schools (comma-separated)")
        motivation_level = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
        outreach_status = st.selectbox("Have you contacted any coaches?", ["No", "Some", "Yes, many"])
        submitted = st.form_submit_button("Get My Game Plan")

    if submitted:
        user_data = {
            "name": name,
            "current_grade_level": current_grade_level,
            "primary_sport": primary_sport,
            "gpa_score": gpa_score,
            "college_targets": college_targets,
            "motivation_level": motivation_level,
            "outreach_status": outreach_status
        }

        missing = validate_user_fields(user_data)
        if missing:
            st.error(f"Missing required fields: {', '.join(missing)}")
        else:
            module = select_module_based_on_input(user_data)
            if module:
                summary = build_summary(user_data, module)
                st.success("✅ Personalized Plan Generated!")
                st.markdown(f"### 🎯 Recommended Module: **{module['name']}**")
                st.markdown("#### 📄 Summary:")
                st.text_area("Summary", summary, height=250)
                if st.button("📥 Download My Game Plan (PDF)"):
                    pdf_path = generate_pdf_from_chat(summary)
                    with open(pdf_path, "rb") as f:
                        st.download_button(label="Download PDF", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")
            else:
                st.warning("No module is currently enabled or applicable for your info. Please check back later.")
