import streamlit as st
import importlib

from interface import template_manager, dashboard, linkedin_post, report_generator

st.set_page_config(page_title="HRAssistant", layout="wide")
st.title("HRAssistant: HR AI Platform")

menu = st.sidebar.radio("Menu", [
    "Create/Edit Offers",
    "Configure Offer Criteria",
    "Manage Templates",
    "Generate LinkedIn Post",
    "Generate CV Report",
    "Match & Ranking Dashboard"
], key="main_menu")

if menu == "Create/Edit Offers":
    import interface.offer_editor
    importlib.reload(interface.offer_editor)
elif menu == "Configure Offer Criteria":
    import interface.filters_config
    importlib.reload(interface.filters_config)
elif menu == "Manage Templates":
    import interface.template_manager
    template_manager.show_template_manager()
elif menu == "Generate LinkedIn Post":
    import interface.linkedin_post
    linkedin_post.show_linkedin_post()
elif menu == "Generate CV Report":
    import interface.report_generator
    report_generator.show_report_generator()
elif menu == "Match & Ranking Dashboard":
    import interface.dashboard
    dashboard.show_dashboard()
