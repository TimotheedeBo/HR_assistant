import importlib

import streamlit as st

st.set_page_config(page_title="HRAssistant Final", layout="wide")
st.title("HRAssistant: HR AI Platform")

menu = st.sidebar.radio("Menu", [
    "Create/Edit Offers",
    "Configure Offer Criteria",
    "Manage Templates",
    "Match & Ranking Dashboard"
])

if menu == "Create/Edit Offers":
    import interface.offer_editor
    importlib.reload(interface.offer_editor)
elif menu == "Configure Offer Criteria":
    import interface.filters_config
    importlib.reload(interface.filters_config)
elif menu == "Manage Templates":
    import interface.template_manager
    importlib.reload(interface.template_manager)
elif menu == "Match & Ranking Dashboard":
    import interface.dashboard
    importlib.reload(interface.dashboard)
