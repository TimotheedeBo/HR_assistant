# interface/filters_config.py

import streamlit as st
import os
import json

def list_offer_ids():
    jobs_dir = "data/jobs"
    return [
        f.replace(".txt", "")
        for f in os.listdir(jobs_dir)
        if f.endswith(".txt")
    ]

def load_criteria(offer_id: str) -> dict:
    path = os.path.join("data/jobs/offer_criteria", f"{offer_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "required_skills": [],
        "required_degree": "",
        "min_years_experience": 0,
        "preferred_skills": []
    }

def save_criteria(offer_id: str, criteria: dict):
    os.makedirs("data/jobs/offer_criteria", exist_ok=True)
    path = os.path.join("data/jobs/offer_criteria", f"{offer_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(criteria, f, indent=2)

def show_filters_config():
    st.header("Configure Offer Criteria / Filters")

    # Make sure folders exist
    os.makedirs("data/jobs/offer_criteria", exist_ok=True)

    offer_ids = list_offer_ids()
    if not offer_ids:
        st.warning("No job offers found. Create offers first.")
        return

    # 1) Select offer
    selected_offer = st.selectbox(
        "Select Job Offer",
        [""] + offer_ids,
        key="filters_offer_select"
    )
    if not selected_offer:
        st.info("Please select an offer to configure its filters.")
        return

    # 2) Load or initialize criteria
    criteria = load_criteria(selected_offer)

    # 3) Form for editing criteria
    form_key = f"filters_form_{selected_offer}"
    with st.form(key=form_key):
        req_skills = st.text_area(
            "Required Skills (comma-separated)",
            value=",".join(criteria.get("required_skills", [])),
            key=f"filters_req_skills_{selected_offer}"
        )
        req_degree = st.text_input(
            "Required Degree",
            value=criteria.get("required_degree", ""),
            key=f"filters_req_degree_{selected_offer}"
        )
        min_years = st.number_input(
            "Minimum Years of Experience",
            value=criteria.get("min_years_experience", 0),
            min_value=0,
            step=1,
            key=f"filters_min_years_{selected_offer}"
        )
        pref_skills = st.text_area(
            "Preferred Skills (comma-separated)",
            value=",".join(criteria.get("preferred_skills", [])),
            key=f"filters_pref_skills_{selected_offer}"
        )

        # Submit button
        submitted = st.form_submit_button(
            "Save Criteria",
            key=f"filters_save_btn_{selected_offer}"
        )

    # 4) After submission
    if submitted:
        new_criteria = {
            "required_skills": [
                s.strip() for s in req_skills.split(",") if s.strip()
            ],
            "required_degree": req_degree.strip(),
            "min_years_experience": int(min_years),
            "preferred_skills": [
                s.strip() for s in pref_skills.split(",") if s.strip()
            ]
        }
        save_criteria(selected_offer, new_criteria)
        st.success(f"Criteria saved for offer: **{selected_offer}**")
