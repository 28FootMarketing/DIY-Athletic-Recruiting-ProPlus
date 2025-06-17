
import streamlit as st
import os
import json
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
from pathlib import Path
# Set Streamlit page configuration
st.set_page_config(page_title="DIY Recruiting-ProPlus", layout="wide")
# Inject custom CSS styling
if Path("styles.css").exists():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Load environment variables
load_dotenv()
# Sidebar Navigation
page = st.sidebar.radio("Navigate", [" Home", " Roadmap", " Admin Panel"])
# Roadmap Content
if page == " Roadmap":
st.title(" DIY Recruiting-ProPlus Roadmap")
st.markdown("Here is what we are working on to improve your recruiting journey.")
st.markdown("""### Upcoming Features by Category:
- **Recruiting Tools**
- Athlete Resume Builder
- Video Audit Module
- **Coach Communication**
- AI Email Feedback
- Cold Outreach Script Generator
- **Motivation & Mindset**
- Mental Performance Journal
- Athlete Reset Toolkit
- **Parent & Coach Hub**
- Weekly Planner Sync
- Parent Communication Scripts
""")
st.stop()
# Admin Panel
is_admin = False
if page == " Admin Panel":
st.title(" Admin Module Control Panel")
password = st.text_input("Enter Admin Password", type="password")
if password == os.getenv("ADMIN_PASSWORD", "admin123"):
is_admin = True
st.success("Access granted.")
else:
st.warning("Enter the correct admin password to manage modules.")
# Home / Main App
if page == " Home" or is_admin:
st.title(" DIY Athletic Recruiting-ProPlus")
st.subheader("Your step-by-step recruiting assistant")
st.markdown("Stay focused, stay ready. Lets keep building. ")
# Athlete Info Form
with st.form("user_input_form"):
st.write("### Athlete Info")
name = st.text_input("Full Name")
current_grade_level = st.selectbox("Grade Level", ["9", "10", "11", "12", "Post Grad"])
primary_sport = st.selectbox("Primary Sport", ["Football", "Basketball", "Baseball", "Softball",
"Soccer", "Track", "Wrestling", "Volleyball", "Esports", "Other"])
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
summary = build_summary(user_data, module)
st.success(" Personalized Plan Generated!")
st.markdown(f"### Recommended Module: **{module}**")
st.markdown("#### Summary:")
st.text_area("Summary", summary, height=250)
if st.button(" Download My Game Plan (PDF)"):
pdf_path = generate_pdf_from_chat(summary)
with open(pdf_path, "rb") as f:
st.download_button(label="Download PDF", data=f, file_name=os.path.basename(pdf_path),
mime="application/pdf")
# Admin: Toggle Modules + View Content
if is_admin:
st.sidebar.markdown("### Toggle & Preview Modules")
toggles = load_module_toggles()
modules = load_ranked_modules()
selected_module_name = st.sidebar.selectbox("Select Module to View", [mod["name"] for mod in modules])
updated = False
for mod in modules:
current = toggles.get(str(mod["id"]), True)
new = st.sidebar.checkbox(f"{mod['id']}. {mod['name']}", value=current)
if new != current:
toggles[str(mod["id"])] = new
updated = True
if updated:
save_module_toggles(toggles)
st.sidebar.success("Module toggles updated!")
selected = next((m for m in modules if m["name"] == selected_module_name), None)
if selected:
st.markdown("---")
st.markdown(f"## Module Preview: {selected['name']}")
st.markdown(f"**Category:** {selected['category']}")
st.markdown(f"**Description:**
{selected['content']}")
