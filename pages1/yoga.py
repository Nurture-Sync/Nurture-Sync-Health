import streamlit as st
import os
from PIL import Image

# Descriptions for Diabetes Mudras and Yoga Poses
diabetes_mudra_descriptions = {
    "apana mudra": "This mudra helps in the purification of the body and stimulates the energy flow to maintain blood sugar levels.",
    "linga mudra": "Linga mudra generates heat in the body, aiding in metabolism and improving pancreatic function.",
    "prana mudra": "Prana mudra activates the energy in the body and improves overall vitality, beneficial for diabetes management.",
    "surya mudra": "Surya mudra enhances the metabolic rate, which can be helpful in controlling blood sugar levels."
}

diabetes_yoga_descriptions = {
    "bow pose": "Bow Pose stretches the pancreas and helps in improving the function of abdominal organs, aiding in digestion.",
    "child pose": "Child Pose calms the mind and relieves stress, which is crucial for diabetes management.",
    "forward bend pose": "Forward Bend Pose helps in massaging the abdominal organs, enhancing digestion and insulin regulation.",
    "half lord of the fishes pose": "This twisting pose stimulates the digestive system and pancreas, aiding in better glucose metabolism."
}

# Descriptions for Thyroid Mudras and Yoga Poses
thyroid_mudra_descriptions = {
    "shankh mudra": "Shankh Mudra regulates the functioning of the thyroid gland and balances the endocrine system.",
    "shunya mudra": "Shunya Mudra helps in calming the mind and can balance hormonal fluctuations associated with thyroid issues.",
    "surya mudra": "Surya Mudra increases heat and improves metabolism, which can aid in managing thyroid problems.",
    "prana mudra": "Prana Mudra enhances the flow of life energy in the body and supports overall thyroid health."
}

thyroid_yoga_descriptions = {
    "camel pose": "Camel Pose stretches the neck region and stimulates the thyroid gland, improving hormone production.",
    "cat-cow pose": "Cat-Cow Pose provides a gentle massage to the thyroid gland and boosts circulation to the neck area.",
    "cobra pose": "Cobra Pose stimulates the thyroid gland and improves blood flow to the neck and chest region.",
    "shavasana": "Shavasana helps in reducing stress and balancing hormones, which is beneficial for thyroid health."
}

# Function to display images with headings and descriptions in two columns
def display_images_with_descriptions(directory_path, descriptions, image_size=(300, 300)):
    image_files = [
        file for file in os.listdir(directory_path)
        if file.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'))
    ]

    for i in range(0, len(image_files), 2):
        cols = st.columns(2)
        
        if i < len(image_files):
            image_path = os.path.join(directory_path, image_files[i])
            image = Image.open(image_path).resize(image_size)
            pose_name = os.path.splitext(image_files[i])[0].replace('_', ' ').lower()
            description = descriptions.get(pose_name, "Description not available")
            
            cols[0].image(image, use_container_width=True)
            cols[0].markdown(f"<h3 style='text-align: center;'>{pose_name.upper()}</h3>", unsafe_allow_html=True)
            cols[0].write(description)

        if i + 1 < len(image_files):
            image_path = os.path.join(directory_path, image_files[i + 1])
            image = Image.open(image_path).resize(image_size)
            pose_name = os.path.splitext(image_files[i + 1])[0].replace('_', ' ').lower()
            description = descriptions.get(pose_name, "Description not available")
            
            cols[1].image(image, use_container_width=True)
            cols[1].markdown(f"<h3 style='text-align: center;'>{pose_name.upper()}</h3>", unsafe_allow_html=True)
            cols[1].write(description)

# Main app
st.title("Yoga Suggestions for Health Management")

# Page selection logic
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation
if st.session_state.page == "home":
    st.header("Select a Health Condition")
    option = st.radio("Choose the condition you want exercises for:", ["Diabetics", "Thyroid"])
    if st.button("Proceed"):
        st.session_state.page = option.lower()

elif st.session_state.page == "diabetics":
    st.header("Yoga and Mudra for Diabetics")
    sub_option = st.radio("Choose an exercise type:", ["Mudra", "Yoga Poses"])

    if sub_option == "Mudra":
        st.write("**Mudra for Diabetics**: These hand gestures help in regulating blood sugar levels and reducing stress.")
        display_images_with_descriptions("C:\\Users\\91948\\Desktop\\Sem5\\cloud projet\\images_diabetics\\Mudra", diabetes_mudra_descriptions)
    elif sub_option == "Yoga Poses":
        st.write("**Yoga Poses for Diabetics**: These poses improve insulin sensitivity and promote relaxation.")
        display_images_with_descriptions("C:\\Users\\91948\\Desktop\\Sem5\\cloud projet\\images_diabetics\\Yoga poses", diabetes_yoga_descriptions)

elif st.session_state.page == "thyroid":
    st.header("Yoga and Mudra for Thyroid")
    sub_option = st.radio("Choose an exercise type:", ["Mudra", "Yoga Poses"])

    if sub_option == "Mudra":
        st.write("**Mudra for Thyroid**: These hand gestures help stimulate the thyroid gland and balance hormone production.")
        display_images_with_descriptions("C:\\Users\\91948\\Desktop\\Sem5\\cloud projet\\images_Thyroid\\Mudra", thyroid_mudra_descriptions)
    elif sub_option == "Yoga Poses":
        st.write("**Yoga Poses for Thyroid**: These poses activate and regulate the thyroid gland for better hormonal balance.")
        display_images_with_descriptions("C:\\Users\\91948\\Desktop\\Sem5\\cloud projet\\images_Thyroid\\Yoga pose", thyroid_yoga_descriptions)

# Button to go back to home page
if st.button("Back to Home"):
    st.session_state.page = "home"
