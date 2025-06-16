"""
app.py
Main Streamlit app with admin module toggle capability
"""

import streamlit as st
import os
from dotenv import load_dotenv
from utils.logic import validate_user_fields, select_module_based_on_input
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat
from utils.module_config import load_module_config, save_module_config

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="DIY Recruiting-ProPlus", layout="wide")

# ✅ Inject custom CSS styling
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found.")

# ✅ Load environment variables
load_dotenv()

# ✅ App Header
st.title("🏅 DIY Athletic Recruiting-ProPlus")
st.subheader("Your step-by-step recruiting assistant")
st.markdown("Stay focused, stay ready. Let’s keep building. 💪🏽")

# ✅ Admin Access
st.sidebar.title("Admin Panel")
admin_code = st.sidebar.text_input("Admin Access Code", type="password")
is_admin = (admin_code == "letmein")  # Replace with your real code

# ✅ Load module toggles
module_config = load_module_config()

# ✅ Admin UI: Toggle modules
if is_admin:
    st.sidebar.subheader("Toggle Modules On/Off")
    for module in module_config:
        module_config[module] = st.sidebar.checkbox(module, module_config[module])
    save_module_config(module_config)
    st.sidebar.success("Module configuration saved.")

# ✅ Filter active modules
active_modules = [k for k, v in module_config.items() if v]

# ✅ State Management
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "module" not in st.session_state:
    st.session_state.module = ""

# ✅ User Info Form
if not st.session_state.submitted:
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
            if module not in active_modules:
                module = active_modules[0] if active_modules else "No active modules available"
            summary = build_summary(user_data, module)

            st.session_state.submitted = True
            st.session_state.user_data = user_data
            st.session_state.summary = summary
            st.session_state.module = module
            st.rerun()

# ✅ Show Summary & Module Tabs
if st.session_state.submitted:
    tab1, tab2 = st.tabs(["📋 Summary", "🚀 Next Module"])

    with tab1:
        st.success("✅ Personalized Plan Generated!")
        st.markdown(f"### 🎯 Recommended Module: **{st.session_state.module}**")
        st.markdown("#### 📄 Summary:")
        st.text_area("Summary", st.session_state.summary, height=250)

        if st.button("📥 Download My Game Plan (PDF)"):
            pdf_buffer = generate_pdf_from_chat(st.session_state.summary)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="recruiting_plan.pdf",
                mime="application/pdf"
            )

    with tab2:
        st.markdown(f"### Welcome to the **{st.session_state.module}** Module")
        st.markdown("This module will guide you step-by-step. Make sure to follow the checklist and stay consistent.")
        st.markdown("📌 Coming soon: embedded checklists, templates, and planners for each module.")

    st.markdown("---")
    st.info("You can get started at [https://recruit.facilitatetheprocess.com](https://recruit.facilitatetheprocess.com) to stay organized and visible to college coaches.")
