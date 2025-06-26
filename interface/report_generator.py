import streamlit as st
import os
from cv_parser.loader import load_cv
from cv_parser.validation import get_cv_text_from_docs
from cv_parser.extractor import extract_cv_data
from utils.report_generator import generate_cv_report
from job_matching.filters import get_offer_criteria

st.header("Generate CV Reports")

# Select CV and Offer
cv_files = [f for f in os.listdir('data/cvs') if f.endswith(('.pdf', '.txt'))]
offers = [f.replace('.txt', '') for f in os.listdir('data/jobs') if f.endswith('.txt')]
cv_sel = st.selectbox("Select CV", cv_files, key='rep_cv')
off_sel = st.selectbox("Select Offer", offers, key='rep_offer')

if cv_sel and off_sel:
    # load and parse CV
    if cv_sel.endswith('.txt'):
        raw = open(f'data/cvs/{cv_sel}', 'r', encoding='utf-8').read()
    else:
        docs = load_cv(f'data/cvs/{cv_sel}')
        raw = get_cv_text_from_docs(docs, cv_sel)
    cv_data = extract_cv_data(raw)
    # load offer & criteria
    offer_text = open(f'data/jobs/{off_sel}.txt', 'r', encoding='utf-8').read()
    criteria = get_offer_criteria(off_sel, 'data/jobs/offer_criteria')

    if st.button("Generate Report"):
        out = generate_cv_report(os.path.splitext(cv_sel)[0], cv_data, off_sel, offer_text, criteria, 'output/')
        st.success(f"Report created: {out}")