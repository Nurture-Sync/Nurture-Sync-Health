import streamlit as st
from db_utils import get_posts

def showPosts():
    st.title("Community Posts")
    posts = get_posts()
    for post in posts:
        st.subheader(post["title"])
        st.write(post["content"])
        
        # Display image if `image_url` exists
        if "image_url" in post:
            st.image(post["image_url"], use_column_width=True)
