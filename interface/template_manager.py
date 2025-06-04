import streamlit as st
import os

TEMPLATES_DIR = "data/templates"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

st.header("Manage CV Templates")

templates = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".docx")]
template_choice = st.selectbox("Existing Templates", [""] + templates)

if template_choice:
    st.write(f"Selected template: {template_choice}")
    if st.button("Delete Template"):
        os.remove(os.path.join(TEMPLATES_DIR, template_choice))
        st.success("Template deleted.")
        st.experimental_rerun()

st.markdown("## Upload New Template")
uploaded_file = st.file_uploader("Upload .docx file", type=["docx"])
if uploaded_file:
    save_path = os.path.join(TEMPLATES_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Template '{uploaded_file.name}' uploaded.")