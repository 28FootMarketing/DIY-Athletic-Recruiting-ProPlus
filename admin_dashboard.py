"""
admin_dashboard.py
Visual dashboard for admins to manage modules.json content.
"""

import streamlit as st
import json

MODULE_FILE = "modules.json"

def load_modules():
    try:
        with open(MODULE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_modules(modules):
    with open(MODULE_FILE, "w") as f:
        json.dump(modules, f, indent=4)

st.title("📊 Admin Module Dashboard")

admin_code = st.text_input("Admin Access Code", type="password")
if admin_code != "letmein":
    st.stop()

modules = load_modules()

st.subheader("Toggle Module Access and Info")
for module, config in modules.items():
    with st.expander(module):
        config["active"] = st.checkbox("Active", value=config["active"], key=module+"-active")
        config["description"] = st.text_area("Description", value=config["description"], key=module+"-desc")
        config["url"] = st.text_input("Module URL", value=config["url"], key=module+"-url")
        config["tier"] = st.selectbox("Available For Tier", ["Role-Player", "Starter", "Captain"], index=["Role-Player", "Starter", "Captain"].index(config["tier"]), key=module+"-tier")

if st.button("💾 Save Module Settings"):
    save_modules(modules)
    st.success("Module settings updated successfully.")
