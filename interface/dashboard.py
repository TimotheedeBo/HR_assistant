import streamlit as st
import os
import json
import pandas as pd
from utils.general import load_text_file
from job_matching.filters import get_offer_criteria, passes_hard_filters
from job_matching.matcher import cosine_score
from cv_parser.extractor import extract_cv_data

CVS_DIR = "data/cvs"
OFFERS_DIR = "data/jobs"
CRITERIA_DIR = "data/jobs/offer_criteria"


def show_dashboard():
    st.header("Match & Ranking Dashboard with Feedback & Export")

    # Load offers & criteria
    offer_ids = [f.replace('.txt','') for f in os.listdir(OFFERS_DIR) if f.endswith('.txt')]
    offers = {oid: load_text_file(os.path.join(OFFERS_DIR,f"{oid}.txt")) for oid in offer_ids}
    criteria_map = {oid: get_offer_criteria(oid, CRITERIA_DIR) for oid in offer_ids}

    # Load & parse CVs
    cv_files = [f for f in os.listdir(CVS_DIR) if f.endswith(('.pdf','.txt'))]
    cv_data = {}
    for cv_file in cv_files:
        path = os.path.join(CVS_DIR, cv_file)
        raw = ""
        if cv_file.endswith('.txt'):
            raw = load_text_file(path)
        else:
            docs = __import__('cv_parser.loader', fromlist=['load_cv']).load_cv(path)
            raw = __import__('cv_parser.validation', fromlist=['get_cv_text_from_docs']).get_cv_text_from_docs(docs, cv_file)
        cv_data[os.path.splitext(cv_file)[0]] = extract_cv_data(raw)

    # Select offer
    selected = st.selectbox("Select Job Offer", offer_ids)
    crit = criteria_map[selected]
    offer_text = offers[selected]

    # Compute matches
    matches = []
    for cid, data in cv_data.items():
        if not passes_hard_filters(data, crit):
            continue
        txt = ", ".join(str(v) for v in data.values())
        score = cosine_score(txt, offer_text)
        matches.append((cid, score))
    matches.sort(key=lambda x: x[1], reverse=True)

    # Display
    if matches:
        df = pd.DataFrame(matches, columns=["cv_id","score"])
        st.dataframe(df)

        st.markdown("### Feedback")
        feedback = {}
        for cid, _ in matches:
            feedback[cid] = st.text_input(f"Feedback for {cid}")

        if st.button("Export Matches to CSV"):
            df.to_csv("output/matches_export.csv", index=False)
            st.success("Exported to output/matches_export.csv")

        if st.button("Save Feedback"):
            fp = os.path.join("output", f"feedback_{selected}.json")
            with open(fp, 'w') as f:
                json.dump(feedback, f, indent=2)
            st.success(f"Feedback saved to {fp}")
    else:
        st.info("No matching CVs found.")

