import streamlit as st
from db_utils import add_post

def NewPost():
    st.title("Create a New Post")
    user_id = st.text_input("User ID")
    title = st.text_input("Post Title")
    content = st.text_area("Post Content")
    if st.button("Submit Post"):
        add_post(user_id, title, content)
        st.success("Post submitted successfully.")
