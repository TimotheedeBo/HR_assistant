# interface/template_manager.py

import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

TEMPLATES_DIR = "data/templates"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

def show_template_manager():
    st.header("Manage CV Templates")

    uploaded_file = st.file_uploader("Upload .docx file", type=["docx"])
    if uploaded_file:
        path = os.path.join(TEMPLATES_DIR, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")

    templates = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".docx")]
    choice = st.selectbox("Existing Templates", [""] + templates)
    if choice and st.button("Delete Template"):
        os.remove(os.path.join(TEMPLATES_DIR, choice))
        st.success(f"Deleted {choice}")

# no top-level st.* calls here
