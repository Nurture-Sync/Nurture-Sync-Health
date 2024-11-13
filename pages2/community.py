import streamlit as st
from db_utils import get_events

def show():
    st.title("Community Landing Page")
    
    st.subheader("Event Calendar")
    events = get_events()
    date_events = {event["date"]: event["title"] for event in events}

    # Display calendar (using a date input as a simple example)
    selected_date = st.date_input("Choose a date")
    if selected_date in date_events:
        st.info(f"Event on {selected_date}: {date_events[selected_date]}")
    else:
        st.info("No events on this day.")
    
    st.subheader("Live Q&A Session")
    st.video("https://youtu.be/yBLY0j8VPrE?feature=shared")  # Replace with actual video link
