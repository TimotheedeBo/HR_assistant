import streamlit as st
import os

CVS_DIR = "data/cvs"
os.makedirs(CVS_DIR, exist_ok=True)

def show_cv_uploader():
    st.header("📂 Upload Candidate CVs")
    st.write("Drop in one or more PDF/TXT/DOCX resumes to ingest them into the system.")

    uploaded = st.file_uploader(
        "Select CV files",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        key="cv_upload"
    )
    if uploaded:
        if st.button("Save CVs", key="cv_save"):
            saved = []
            for f in uploaded:
                # sanitize filename
                fn = f.name.replace(" ", "_")
                path = os.path.join(CVS_DIR, fn)
                with open(path, "wb") as out:
                    out.write(f.getbuffer())
                saved.append(fn)
            st.success(f"Saved {len(saved)} file(s): {', '.join(saved)}")
