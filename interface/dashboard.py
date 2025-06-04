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

st.header("Match & Ranking Dashboard with Feedback & Export")

# Load offers
offer_ids = [f.replace(".txt", "") for f in os.listdir(OFFERS_DIR) if f.endswith(".txt")]
offers = {oid: load_text_file(os.path.join(OFFERS_DIR, f"{oid}.txt")) for oid in offer_ids}
offer_criteria = {oid: get_offer_criteria(oid, CRITERIA_DIR) for oid in offer_ids}

# Load CVs
cv_files = [f for f in os.listdir(CVS_DIR) if f.endswith(".pdf") or f.endswith(".txt")]
cv_data = {}
for cv_file in cv_files:
    path = os.path.join(CVS_DIR, cv_file)
    if cv_file.endswith(".txt"):
        raw = load_text_file(path)
    else:
        try:
            from cv_parser.loader import load_cv
            docs = load_cv(path)
            from cv_parser.validation import get_cv_text_from_docs
            raw = get_cv_text_from_docs(docs, cv_file)
        except Exception:
            raw = ""
    cv_id = os.path.splitext(cv_file)[0]
    cv_data[cv_id] = extract_cv_data(raw)

# Selected offer
selected_offer = st.selectbox("Select Job Offer", offer_ids)
criteria = offer_criteria[selected_offer]
offer_text = offers[selected_offer]

matches = []
for cv_id, cv in cv_data.items():
    if not passes_hard_filters(cv, criteria):
        continue
    score = cosine_score(", ".join([str(v) for v in cv.values()]), offer_text)
    matches.append((cv_id, score))

matches.sort(key=lambda x: x[1], reverse=True)

# Display matches
st.write("## Matching CVs:")
if matches:
    df = pd.DataFrame(matches, columns=["cv_id", "score"])
    st.dataframe(df)

    # Feedback inputs
    st.markdown("### Provide Feedback")
    feedback = {}
    for cv_id, score in matches:
        fb = st.text_input(f"Feedback for {cv_id}", key=f"fb_{cv_id}")
        feedback[cv_id] = fb

    # Export to CSV
    if st.button("Export Matches to CSV"):
        df.to_csv("output/matches_export.csv", index=False)
        st.success("Exported to output/matches_export.csv")

    # Show feedback JSON
    if st.button("Save Feedback"):
        fb_path = os.path.join("output", f"feedback_{selected_offer}.json")
        with open(fb_path, "w", encoding="utf-8") as f:
            json.dump(feedback, f, indent=2)
        st.success(f"Feedback saved to {fb_path}")
else:
    st.info("No matching CVs found for this offer based on current criteria.")
