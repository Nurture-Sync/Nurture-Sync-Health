import streamlit as st
from auth.firebase_auth import sign_up_with_email_and_password, sign_in_with_email_and_password, reset_password
from streamlit_lottie import st_lottie
import requests
import json
import re

# Function to load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottie_local(path: str):
    with open(path, "r") as file:
        return json.load(file)

# Load Lottie animation from the local assets folder
lottie_path = "./assets/lottie_animation.json"
lottie_animation = load_lottie_local(lottie_path)

# Inject custom CSS for styling
def add_custom_css():
    st.markdown("""
        <style>
        body { background-color: #f0f2f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .stButton button { background-color: #4CAF50; color: white; font-size: 16px; border: none; padding: 12px 24px; cursor: pointer; border-radius: 5px; transition: background-color 0.3s ease; }
        .stButton button:hover { background-color: #45a049; }
        .stTextInput input, .stSelectbox select { font-size: 16px; padding: 12px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 20px; width: 100%; }
        .stTextArea textarea { font-size: 16px; padding: 12px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 20px; width: 100%; }
        .stSuccess { color: green; }
        .stWarning { color: red; }
        .lottie { margin: auto; display: block; }
        .forgot-password { font-size: 14px; color: #0066CC; text-decoration: underline; cursor: pointer; }
        .forgot-password:hover { color: #004C99; }
        </style>
    """, unsafe_allow_html=True)

# Validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Validate password strength
def is_strong_password(password):
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$'
    return re.match(password_regex, password) is not None

# Streamlit landing page
def app():
    add_custom_css()
    st.title("Welcome to NurtureSync")

    # Display Lottie animation
    st_lottie(lottie_animation, speed=1, width=600, height=400, key="landing")

    # Initialize session state variables
    if "signed_in" not in st.session_state:
        st.session_state.signed_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "forgot_password" not in st.session_state:
        st.session_state.forgot_password = False
    if "password_reset_successful" not in st.session_state:
        st.session_state.password_reset_successful = False

    # Authentication options
    if not st.session_state.signed_in:
        choice = st.selectbox('Choose an action', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        
        email_error = None
        password_error = None

        # Validate email
        if email and not is_valid_email(email):
            email_error = "Invalid email format."

        # Validate password
        if password and not is_strong_password(password):
            password_error = "Password must have at least 6 characters, one uppercase, one number, and one special character."

        if choice == 'Sign up':
            username = st.text_input("Username")
            if st.button('Create Account'):
                if not email or email_error:
                    st.warning(email_error or "Please provide a valid email.")
                elif not password or password_error:
                    st.warning(password_error or "Invalid password.")
                elif not username:
                    st.warning("Username is required.")
                else:
                    with st.spinner("Creating account..."):
                        sign_up_response = sign_up_with_email_and_password(email=email, password=password, username=username)
                    if 'error' in sign_up_response:
                        st.warning(f"Signup failed: {sign_up_response.get('message', 'Error occurred')}")
                    else:
                        st.success('Account created! Please Login.')

        elif choice == 'Login':
            if st.button('Login'):
                if not email or email_error:
                    st.warning(email_error or "Please enter a valid email.")
                elif not password:
                    st.warning("Password cannot be empty.")
                else:
                    with st.spinner("Logging in..."):
                        login_response = sign_in_with_email_and_password(email=email, password=password)
                    if 'error' in login_response:
                        st.warning(f"Login failed: {login_response.get('message', 'Error occurred')}")
                    else:
                        st.session_state.signed_in = True
                        st.session_state.username = login_response.get('displayName', email)
                        st.success(f"Welcome, {st.session_state.username}")

            # Forgot password section
            if st.button('Forgot Password?'):
                st.session_state.forgot_password = True

            if st.session_state.forgot_password and not st.session_state.password_reset_successful:
                with st.form(key='reset_password_form'):
                    # Autofill email in the reset email field if available
                    reset_email = st.text_input('Enter your email for password reset', value=email if email else '')
                    submit_button = st.form_submit_button(label='Send Reset Password Email')

                    if submit_button:
                        if not reset_email:
                            st.warning("Please enter an email.")
                        elif not is_valid_email(reset_email):
                            st.warning("Invalid email.")
                        else:
                            with st.spinner("Sending reset email..."):
                                try:
                                    # Call the reset password function
                                    success, message = reset_password(reset_email)
                                    if success:
                                        st.success("Password reset email sent.")
                                        st.session_state.password_reset_successful = True  # Mark reset as successful
                                        st.rerun()  # Refresh the page to hide the reset form
                                    else:
                                        st.warning(f"Error: {message}")
                                except Exception as e:
                                    st.error(f"An error occurred: {str(e)}")

    # Signed-in state
    if st.session_state.signed_in:
        st.text(f"Welcome back, {st.session_state.username}")
        if st.button('Sign out'):
            st.session_state.update(signed_in=False, username=None)
            st.success("Signed out successfully.")
            st.rerun()  # Refresh the page

# Run the app
if __name__ == "__main__":
    app()
