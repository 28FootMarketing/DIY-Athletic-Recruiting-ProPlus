import streamlit as st
import os
from dotenv import load_dotenv
from utils.logic import validate_user_fields, select_module_based_on_input
from utils.summary import build_summary
from utils.pdf_generator import generate_pdf_from_chat

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="DIY Recruiting-ProPlus", layout="wide")

# ✅ Inject custom CSS styling
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# ✅ Load environment variables (if needed)
load_dotenv()

# ✅ App Header
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

# ✅ Logic after submission
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

    # Validate input
    missing = validate_user_fields(user_data)
    if missing:
        st.error(f"Missing required fields: {', '.join(missing)}")
    else:
        module = select_module_based_on_input(user_data)
        summary = build_summary(user_data, module)

        st.success("✅ Personalized Plan Generated!")
        st.markdown(f"### 🎯 Recommended Module: **{module}**")
        st.markdown("#### 📄 Summary:")
        st.text_area("Summary", summary, height=250)

        if st.button("📥 Download My Game Plan (PDF)"):
            pdf_path = generate_pdf_from_chat(summary)
            with open(pdf_path, "rb") as f:
                st.download_button(label="Download PDF", data=f, file_name=os.path.basename(pdf_path), mime="application/pdf")

        # First-time call-to-action link
        st.markdown("---")
        st.info("You can get started at [https://recruit.facilitatetheprocess.com](https://recruit.facilitatetheprocess.com) to stay organized and visible to college coaches.")
