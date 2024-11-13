import streamlit as st
from db_utils import add_doctor_query, get_doctor_queries, add_community_response

def Discuss():
    st.title("Community Discussion Forum 🗣️")
    st.write("Engage in meaningful discussions on topics related to thyroid, diabetes, and general health.")

    # Forum selection dropdown
    forum_type = st.selectbox("Select a Discussion Forum", ["Diabetes", "Thyroid", "General"])

    # Post a question in the selected forum
    st.header(f"Ask a Question in {forum_type} Forum")
    user_id = st.text_input("Your Username", key="user_id_discuss")
    question = st.text_area("What's your question for the community?", key="question_discuss")
    if st.button("Submit Question"):
        add_doctor_query(user_id, question, forum_type)
        st.success(f"Your question has been posted in the {forum_type} forum!")

    # Display existing questions and responses in the selected forum
    st.header(f"{forum_type} Forum - Community Questions")
    queries = get_doctor_queries(forum_type=forum_type)  # Filter by selected forum type
    if queries:
        for query in queries:
            # Display each question with user ID
            st.markdown(f"**{query['user_id']}** asked:")
            st.markdown(f"*{query['question']}*")

            # Allow community members to respond
            with st.expander("💬 Add a Response", expanded=False):
                responder_id = st.text_input("Your Username", key=f"responder_id_{query['_id']}")
                response = st.text_area("Write your response...", key=f"response_{query['_id']}")
                if st.button("Submit Response", key=f"submit_{query['_id']}"):
                    if response:
                        add_community_response(query['_id'], responder_id, response)
                        st.success("Response submitted!")
                    else:
                        st.warning("Please type a response before submitting.")

            # Display existing responses to the question
            if query["responses"]:
                st.markdown("### Responses")
                for response_data in query["responses"]:
                    st.markdown(f"**{response_data['responder_id']}** responded:")
                    st.markdown(f"> {response_data['response']}")
            else:
                st.info("No responses yet.")
    else:
        st.info(f"There are no questions in the {forum_type} forum at the moment.")
