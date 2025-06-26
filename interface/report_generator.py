import streamlit as st
import os
from cv_parser.loader import load_cv
from cv_parser.validation import get_cv_text_from_docs
from cv_parser.extractor import extract_cv_data
from utils.report_generator import generate_cv_report
from job_matching.filters import get_offer_criteria
from utils.general import load_text_file
from dotenv import load_dotenv
load_dotenv()

CV_DIR = 'data/cvs'
JOB_DIR = 'data/jobs'
CRIT_DIR = 'data/jobs/offer_criteria'

def show_report_generator():
    st.header("Generate CV Reports")
    cv_files = [f for f in os.listdir(CV_DIR) if f.endswith(('.pdf', '.txt'))]
    offers = [f.replace('.txt', '') for f in os.listdir(JOB_DIR) if f.endswith('.txt')]
    cv_sel = st.selectbox("Select CV", cv_files, key="rep_cv")
    off_sel = st.selectbox("Select Offer", offers, key="rep_offer")

    if cv_sel and off_sel:
        raw = load_text_file(os.path.join(CV_DIR, cv_sel)) if cv_sel.endswith('.txt') else get_cv_text_from_docs(load_cv(os.path.join(CV_DIR, cv_sel)), cv_sel)
        cv_data = extract_cv_data(raw)
        offer_text = load_text_file(os.path.join(JOB_DIR, f"{off_sel}.txt"))
        criteria = get_offer_criteria(off_sel, CRIT_DIR)
        if st.button("Generate Report", key="rep_gen_btn"):
            out = generate_cv_report(os.path.splitext(cv_sel)[0], cv_data, off_sel, offer_text, criteria, 'output/')
            st.success(f"Report created: {out}")
