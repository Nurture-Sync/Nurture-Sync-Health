import streamlit as st
from streamlit_chat import message
import requests
from langchain.memory import ConversationBufferMemory

def setup_syncbot():
    
    # Page Title and Description
    st.title("SyncBot 👩🏻‍⚕")
    st.markdown("""
        **Your AI-powered health assistant**  
        Ask me anything about **Thyroid** and **Diabetes**. I'm here to guide you on your health journey.  
    """)

    # Vext API Configuration
    API_URL = "https://payload.vextapp.com/hook/J1460Z18NT/catch/$(nandiniNShealth)"
    API_KEY = "aoxRWadT.BTsbRkr94z4wgPgbtgnJ7XFx4ldCJlMo"

    # Function to send user input to the Vext API and receive a response
    def get_response_from_vext(user_query):
        headers = {
            "Content-Type": "application/json",
            "Apikey": f"Api-Key {API_KEY}"
        }
        payload = {"payload": user_query}
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response_json = response.json()  # Parse the JSON response
            return response_json.get("text", "No response text available.")
        except requests.exceptions.RequestException as e:
            return f"Error communicating with the API: {str(e)}"

    # Memory for chat history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Initialize session state
    def initialize_session_state():
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello! You can ask me anything about Thyroid and Diabetes 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey! 👋"]

    # Display chat history
    def display_chat_history():
        reply_container = st.container()
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Question:", placeholder="Ask about Thyroid and Diabetes", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                # Fetch response from Vext API
                output = get_response_from_vext(user_input)

                # Update session state
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with reply_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=f"{i}_user", avatar_style="adventurer")
                    message(st.session_state["generated"][i], key=f"{i}", avatar_style="bottts")

    # Initialize session state
    initialize_session_state()

    # Display chat history
    display_chat_history()

# Uncomment the following lines to run the app standalone
# if __name__ == "__main__":
#     setup_syncbot()
