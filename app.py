import streamlit as st
from streamlit_option_menu import option_menu
from pages1.landing_page import app as landing_page_app
from pages1.profile import home1
from pages1.track import track
from pages1.report import report
from pages1.cal_est2 import est2
from pages1.calorie_est import cal_est
from pages1.health_questionnaire import show_patient_questionnaire
from pages2.ask_doctor import Ask_doctor
from pages2.community import show as community_show
from pages2.discussion_forum import Discuss
from pages2.new_post import NewPost
from pages2.post_feed import showPosts

# Initialize session state for first load
if 'selected' not in st.session_state:
    st.session_state.selected = "Landing Page"
if 'community_selected' not in st.session_state:
    st.session_state.community_selected = "Landing Page"

# Main Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Landing Page","Patient Questionnaire", "Profile", "Track", "Report", "Calorie Estimate", "Track Food",   "Community"],
        icons=["house","clipboard-heart", "person-circle", "activity", "file-earmark-arrow-down", "calculator", "basket",   "people"],
        menu_icon="cast",
        default_index=0
    )
    st.session_state.selected = selected  # Update main session state

# Main Navigation Logic
if st.session_state.selected == "Landing Page":
    landing_page_app()
elif st.session_state.selected == "Profile":
    home1()
elif st.session_state.selected == "Track":
    track()
elif st.session_state.selected == "Report":
    report()
elif st.session_state.selected == "Calorie Estimate":
    cal_est()
elif st.session_state.selected == "Track Food":
    est2()
elif st.session_state.selected == "Patient Questionnaire":
    show_patient_questionnaire()
elif st.session_state.selected == "Community":
    # Sidebar navigation for Community section
    with st.sidebar:
        community_selected = option_menu(
            menu_title="Healthcare Community",
            options=["Landing Page", "Post Feed", "New Post", "Discussion Forum", "Ask Doctor"],
            icons=["house", "list", "plus-circle", "chat-left-text", "envelope"],
            default_index=0
        )
        st.session_state.community_selected = community_selected  # Update community session state

    # Community Section Navigation Logic
    if st.session_state.community_selected == "Landing Page":
        community_show()
    elif st.session_state.community_selected == "Post Feed":
        showPosts()
    elif st.session_state.community_selected == "New Post":
        NewPost()
    elif st.session_state.community_selected == "Discussion Forum":
        Discuss()
    elif st.session_state.community_selected == "Ask Doctor":
        Ask_doctor()
