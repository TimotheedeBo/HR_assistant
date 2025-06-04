import streamlit as st
import os
import json

CRITERIA_DIR = "data/jobs/offer_criteria"
os.makedirs(CRITERIA_DIR, exist_ok=True)

def list_offer_ids(): 
    jobs_dir = "data/jobs"
    return [f.replace(".txt", "") for f in os.listdir(jobs_dir) if f.endswith(".txt")]

def load_criteria(offer_id):
    path = os.path.join(CRITERIA_DIR, f"{offer_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"required_skills": [], "required_degree": "", "min_years_experience": 0, "preferred_skills": []}

def save_criteria(offer_id, criteria):
    path = os.path.join(CRITERIA_DIR, f"{offer_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(criteria, f, indent=2)

st.header("Configure Offer Criteria/Filters")

offer_ids = list_offer_ids()
if not offer_ids:
    st.warning("No job offers found. Create offers first.")
    st.stop()

selected_offer = st.selectbox("Select Job Offer", offer_ids)
criteria = load_criteria(selected_offer)

required_skills = st.text_area("Required Skills (comma separated)", value=",".join(criteria.get("required_skills", [])))
required_degree = st.text_input("Required Degree", value=criteria.get("required_degree", ""))
min_years_exp = st.number_input("Minimum Years of Experience", value=criteria.get("min_years_experience", 0), min_value=0, step=1)
preferred_skills = st.text_area("Preferred Skills (comma separated)", value=",".join(criteria.get("preferred_skills", [])))

if st.button("Save Criteria"):
    new_criteria = {
        "required_skills": [s.strip() for s in required_skills.split(",") if s.strip()],
        "required_degree": required_degree,
        "min_years_experience": int(min_years_exp),
        "preferred_skills": [s.strip() for s in preferred_skills.split(",") if s.strip()]
    }
    save_criteria(selected_offer, new_criteria)
    st.success("Criteria updated.")