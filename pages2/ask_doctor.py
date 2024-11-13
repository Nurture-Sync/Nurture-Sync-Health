import streamlit as st
from db_utils import add_doctor_query, get_doctor_queries, add_doctor_response
from bson import ObjectId

def Ask_doctor():
    st.title("Ask a Doctor 💬")
    st.write("Connect with experienced doctors to get answers to your health-related questions.")

    # Section to submit a new question
    st.header("Post Your Question")
    user_id = st.text_input("Your Username", key="user_id_ask")
    question = st.text_area("Type your question for the doctor here...", key="question_ask")
    if st.button("Send Query"):
        add_doctor_query(user_id, question)
        st.success("Your question has been posted! A doctor will respond soon.")

    # Display existing questions and answers
    st.header("Doctor Responses")
    queries = get_doctor_queries()
    if queries:
        for query in queries:
            # Display user question with user ID
            st.markdown(f"**{query['user_id']}** asked:")
            st.markdown(f"*{query['question']}*")

            # Icon for doctor to answer the question
            with st.expander("👨‍⚕️ Respond", expanded=False):
                doctor_id = st.text_input("Doctor ID", key=f"doctor_id_{query['_id']}")
                response = st.text_area("Type your response here...", key=f"response_{query['_id']}")
                if st.button("Submit Response", key=f"submit_{query['_id']}"):
                    if response:
                        add_doctor_response(query['_id'], doctor_id, response)
                        st.success("Response submitted!")
                    else:
                        st.warning("Please type a response before submitting.")

            # Display existing responses for the query
            if query["responses"]:
                st.markdown("### Responses")
                for response_data in query["responses"]:
                    st.markdown(f"**Doctor {response_data['doctor_id']}** responded:")
                    st.markdown(f"> {response_data['response']}")
            else:
                st.info("No responses yet.")
    else:
        st.info("There are no questions at the moment.")
