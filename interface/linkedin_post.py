import streamlit as st
import os
from job_matching.linkedin_agent import generate_linkedin_post
from utils.general import load_text_file
from job_matching.filters import get_offer_criteria

def show_linkedin_post():
    st.header("Generate LinkedIn Announcement")
    offer_ids = [f.replace('.txt', '') for f in os.listdir('data/jobs') if f.endswith('.txt')]
    selected = st.selectbox("Select Offer", offer_ids, key='li_select_offer')

    if selected:
        title, description = load_text_file(f'data/jobs/{selected}.txt').split('\n', 1)
        criteria = get_offer_criteria(selected, 'data/jobs/offer_criteria')
        if st.button("Generate Post"):
            post = generate_linkedin_post(selected, title, description, criteria)
            st.text_area("LinkedIn Post", value=post, height=200)
