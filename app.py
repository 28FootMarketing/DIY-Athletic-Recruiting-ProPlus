
import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.logic import validate_user_fields, select_module_based_on_input
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat
from collections import defaultdict

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="DIY Recruiting-ProPlus", layout="wide")

# ✅ Inject custom CSS styling
if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Load environment variables
load_dotenv()

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["🏠 Main", "📍 Roadmap"])

# Admin login
admin_code = st.sidebar.text_input("Admin Code", type="password")
is_admin = admin_code == "ftproplus2025"  # Customize this

# File path for roadmap
roadmap_file = "roadmap.json"

def load_roadmap():
    try:
        with open(roadmap_file, "r") as f:
            return json.load(f)
    except:
        return []

def save_roadmap(data):
    with open(roadmap_file, "w") as f:
        json.dump(data, f, indent=4)

roadmap = load_roadmap()

# PAGE: MAIN
if page == "🏠 Main":
    st.title("🏅 DIY Athletic Recruiting-ProPlus")
    st.subheader("Your step-by-step recruiting assistant")
    st.markdown("Stay focused, stay ready. Let’s keep building. 💪🏽")

    # ✅ User Info Form
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
            summary = build_summary(user_data, module)

            st.session_state.summary = summary
            st.success("✅ Personalized Plan Generated!")
            st.markdown(f"### 🎯 Recommended Module: **{module}**")
            st.markdown("#### 📄 Summary:")
            st.text_area("Summary", summary, height=250)

            if st.button("📥 Download My Game Plan (PDF)"):
                pdf_path = generate_pdf_from_chat(summary)
                with open(pdf_path, "rb") as f:
                    st.download_button(label="Download PDF", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")

# PAGE: ROADMAP
elif page == "📍 Roadmap":
    st.title("📍 Recruiting Roadmap")
    st.info("Track what’s coming next for DIY Recruiting-ProPlus.")

    roadmap_by_month = defaultdict(list)
    for item in roadmap:
        roadmap_by_month[item["eta"]].append(item)

    for month in sorted(roadmap_by_month):
        st.markdown(f"## 📅 {month}")
        for i, item in enumerate(roadmap_by_month[month]):
            st.markdown(f"### 🔧 {item['feature']}")
            st.markdown(f"- **Status:** `{item['status']}`")
            st.markdown(f"- _{item['description']}_")

            if is_admin:
                if st.button(f"❌ Remove: {item['feature']}", key=f"remove_{month}_{i}"):
                    roadmap.remove(item)
                    save_roadmap(roadmap)
                    st.experimental_rerun()

    if is_admin:
        st.markdown("---")
        st.markdown("### ➕ Add New Feature to Roadmap")
        with st.form("add_feature_form"):
            new_feature = st.text_input("Feature Name")
            new_description = st.text_area("Feature Description")
            new_status = st.selectbox("Status", ["Planned", "In Progress", "Coming Soon", "Released"])
            new_eta = st.date_input("Estimated Launch Date", value=datetime.today())
            submitted = st.form_submit_button("Add Feature")

        if submitted:
            roadmap.append({
                "feature": new_feature,
                "description": new_description,
                "status": new_status,
                "eta": new_eta.strftime("%B %Y")
            })
            save_roadmap(roadmap)
            st.success("✅ Feature added to roadmap.")
            st.experimental_rerun()
