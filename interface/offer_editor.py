import streamlit as st
import os
import json
from utils.general import generate_offer_id

OFFERS_DIR = "data/jobs"
CRITERIA_DIR = "data/jobs/offer_criteria"
os.makedirs(OFFERS_DIR, exist_ok=True)
os.makedirs(CRITERIA_DIR, exist_ok=True)

def get_offer_ids():
    return [f.replace(".txt", "") for f in os.listdir(OFFERS_DIR) if f.endswith(".txt")]

def save_offer(offer_id, title, content):
    path = os.path.join(OFFERS_DIR, f"{offer_id}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{content}")

def create_default_criteria(offer_id):
    path = os.path.join(CRITERIA_DIR, f"{offer_id}.json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "required_skills": [],
                "required_degree": "",
                "min_years_experience": 0,
                "preferred_skills": []
            }, f, indent=2)

st.header("Create or Edit Job Offer")

title = st.text_input("Offer Title")
offer_id = generate_offer_id(title) if title else ""
st.text_input("Offer ID (auto)", value=offer_id, disabled=True)
description = st.text_area("Offer Description (requirements, responsibilities, etc.)")
if st.button("Save Offer"):
    if not title or not description:
        st.error("Title and description required!")
    elif offer_id in get_offer_ids():
        st.error(f"Offer ID '{offer_id}' already exists! Change the title.")
    else:
        save_offer(offer_id, title, description)
        create_default_criteria(offer_id)
        st.success(f"Offer '{offer_id}' created with default criteria file.")

st.markdown("---")
st.info("Go to 'Configure Offer Criteria' to set required/preferred skills and filters for each offer.")