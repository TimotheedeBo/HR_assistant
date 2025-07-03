# interface/template_manager.py

import streamlit as st
import os
from dotenv import load_dotenv

from cv_parser.loader import load_cv
from cv_parser.validation import get_cv_text_from_docs
from cv_parser.extractor import extract_cv_data
from cv_generation.generator import generate_company_cv

load_dotenv()

# Directories
TEMPLATES_DIR = "data/templates"
CVS_DIR      = "data/cvs"
OUTPUT_DIR   = "output"

# Ensure folders exist
for d in (TEMPLATES_DIR, CVS_DIR, OUTPUT_DIR):
    os.makedirs(d, exist_ok=True)

def show_template_manager():
    st.header("Manage CV Templates")

    # -- Upload new template --
    tpl_u = st.file_uploader(
        "Upload Template (.docx or .txt)",
        type=["docx", "txt"],
        key="tpl_upload"
    )
    if tpl_u:
        save_path = os.path.join(TEMPLATES_DIR, tpl_u.name)
        with open(save_path, "wb") as f:
            f.write(tpl_u.getbuffer())
        st.success(f"Template uploaded: {tpl_u.name}")

    # -- Delete existing template --
    templates = [f for f in os.listdir(TEMPLATES_DIR)
                 if f.lower().endswith((".docx", ".txt"))]
    del_choice = st.selectbox(
        "Existing Templates",
        [""] + templates,
        key="tpl_delete_select"
    )
    if del_choice and st.button("Delete Template", key="tpl_delete_btn"):
        os.remove(os.path.join(TEMPLATES_DIR, del_choice))
        st.success(f"Deleted template: {del_choice}")
        st.experimental_rerun()

    st.markdown("---")

    # -- Generate a branded CV from a template --
    st.subheader("Generate Company-Branded CV")

    # 1) Select a candidate CV file
    cvs = [f for f in os.listdir(CVS_DIR)
           if f.lower().endswith((".pdf", ".txt", ".docx"))]
    cv_choice = st.selectbox(
        "Select Candidate CV",
        [""] + cvs,
        key="tpl_cv_select"
    )

    # 2) Select one of the uploaded templates
    tpl_choice = st.selectbox(
        "Select Template",
        [""] + templates,
        key="tpl_gen_select"
    )

    # 3) Generate when both are chosen
    if cv_choice and tpl_choice and st.button("Generate CV", key="tpl_gen_btn"):
        # Load raw CV text
        cv_path = os.path.join(CVS_DIR, cv_choice)
        if cv_choice.lower().endswith(".txt"):
            with open(cv_path, "r", encoding="utf-8") as f:
                raw = f.read()
        elif cv_choice.lower().endswith(".pdf"):
            docs = load_cv(cv_path)
            raw  = get_cv_text_from_docs(docs, cv_choice, logger=st)
        else:  # .docx
            from docx import Document
            docx = Document(cv_path)
            raw  = "\n".join(p.text for p in docx.paragraphs)

        # Parse CV into structured dict via GPT
        data = extract_cv_data(raw)

        # Build paths for your generator signature
        template_path = os.path.join(TEMPLATES_DIR, tpl_choice)
        name_slug     = data.get("name", "unknown").replace(" ", "_")
        out_filename  = f"{name_slug}_{tpl_choice}"
        output_path   = os.path.join(OUTPUT_DIR, out_filename)

        # Fill template and write new CV
        try:
            result_path = generate_company_cv(data, template_path, output_path)
            st.success(f"Generated CV: {result_path}")
            with open(result_path, "rb") as fp:
                st.download_button(
                    "Download Branded CV",
                    fp.read(),
                    file_name=os.path.basename(result_path),
                    key="tpl_download"
                )
        except Exception as e:
            st.error(f"Error generating CV: {e}")
