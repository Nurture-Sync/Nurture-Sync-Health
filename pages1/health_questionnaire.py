# questionnaire.py

import streamlit as st
from pymongo import MongoClient

# MongoDB setup
MONGO_URI = "mongodb+srv://community:NS123456@cluster0.smgpcp9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
patient_db = client["patient_data_db"]  # New database for storing patient data
patient_collection = patient_db["patient_responses"]  # Collection to store responses

# Define the questions and possible answers
questions = {
    "Current Diagnosis": ["Diabetes", "Hypertension", "Asthma", "Other"],
    "Medications": ["Insulin", "Metformin", "Aspirin", "None", "Other"],
    "Dietary Preferences": ["Vegetarian", "Non-Vegetarian", "Vegan", "Gluten-Free", "None"],
    "Exercise Routine": ["Cardio", "Strength Training", "Yoga", "Running", "None"],
    "Health Goals": ["Weight Loss", "Muscle Gain", "Increased Flexibility", "Improved Stamina", "None"],
    "Current Symptoms": ["Fatigue", "Headache", "Dizziness", "Nausea", "Pain", "None"]
}

def show_patient_questionnaire():
    # Initialize session state if not already done
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0  # Start with the first question
        st.session_state.responses = {}

    # Function to handle displaying and collecting answers for a question
    def display_question(question, options):
        # Use multiselect to allow multiple selections
        selected_options = st.multiselect(
            f'Select options for {question}:',
            options=options
        )
        
        if selected_options:
            st.session_state.responses[question] = selected_options
            return True
        return False

    # Logic for displaying questions one by one
    if st.session_state.current_question < len(questions):
        current_question_text = list(questions.keys())[st.session_state.current_question]
        current_options = questions[current_question_text]
        
        # Display current question
        st.subheader(current_question_text)
        
        # Display the question and capture answers
        if display_question(current_question_text, current_options):
            st.success("You selected: " + ", ".join(st.session_state.responses[current_question_text]))
            # Button to move to the next question
            if st.button("Next"):
                st.session_state.current_question += 1  # Move to the next question
    else:
        # After all questions are answered
        st.subheader("Summary of Your Responses:")
        for question, answers in st.session_state.responses.items():
            st.write(f"{question}: {', '.join(answers) if answers else 'No selection made'}")

        # Button to submit the questionnaire
        if st.button("Submit"):
            # Save responses to MongoDB
            patient_data = {
                "responses": st.session_state.responses
            }
            patient_collection.insert_one(patient_data)  # Insert the data into the collection
            st.success("Your responses have been submitted and stored in the database.")
            
            # Optionally, reset session state for another submission
            st.session_state.current_question = 0
            st.session_state.responses = {}
