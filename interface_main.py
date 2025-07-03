import streamlit as st

from interface import template_manager, dashboard, linkedin_post, report_generator, cv_uploader, cv_matcher, \
    offer_editor, filters_config

st.set_page_config(page_title="HRAssistant", layout="wide")
st.title("HRAssistant: HR AI Platform")

menu = st.sidebar.radio("Menu", [
    "Create/Edit Offers",
    "Configure Offer Criteria",
    "Upload CVs",
    "Match CVs",
    "Manage Templates",
    "Generate LinkedIn Post",
    "Generate CV Report",
    "Match & Ranking Dashboard"
], key="main_menu")

if menu == "Create/Edit Offers":
    offer_editor.show_offer_editor()
elif menu == "Configure Offer Criteria":
    filters_config.show_filters_config()
elif menu == "Manage Templates":
    template_manager.show_template_manager()
elif menu == "Upload CVs":
    cv_uploader.show_cv_uploader()
elif menu == "Match CVs":
    cv_matcher.show_cv_matcher()
elif menu == "Generate LinkedIn Post":
    linkedin_post.show_linkedin_post()
elif menu == "Generate CV Report":
    report_generator.show_report_generator()
elif menu == "Match & Ranking Dashboard":
    dashboard.show_dashboard()

