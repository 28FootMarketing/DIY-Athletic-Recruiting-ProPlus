
import streamlit as st
import os
from dotenv import load_dotenv
from utils.logic_admin import (
    validate_user_fields,
    select_module_based_on_input,
    load_module_toggles,
    save_module_toggles
)
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="DIY Recruiting-ProPlus", layout="wide")

# ✅ Load custom CSS
if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Load environment variables
load_dotenv()

# ✅ Sidebar: Admin Module Toggle UI
with st.sidebar.expander("🔐 Admin: Toggle Modules"):
    st.markdown("Enable or disable modules below:")
    module_toggles = load_module_toggles()
    updated_toggles = {}

    for mod_id in sorted(module_toggles.keys(), key=int):
        enabled = st.checkbox(f"Module {mod_id}", value=module_toggles[mod_id])
        updated_toggles[mod_id] = enabled

    if st.button("💾 Save Module Toggles"):
        save_module_toggles(updated_toggles)
        st.success("Module settings updated. Refresh the app to apply changes.")

# ✅ App Header
st.title("🏅 DIY Athletic Recruiting-ProPlus")
st.subheader("Your step-by-step recruiting assistant")
st.markdown("Stay focused, stay ready. Let’s keep building. 💪🏽")

# ✅ Main Form: Athlete Info
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

# ✅ Submission Logic
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

    # Validate required fields
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
            st.warning("No modules available or matching criteria. Please adjust toggle settings or try again.")
