# auth/firebase_auth.py

import firebase_admin
from firebase_admin import credentials, auth
import requests
import json


# Initialize Firebase app only if not already initialized
def initialize_firebase():
    if not firebase_admin._apps:
        # Provide the path to your service account JSON file
        cred = credentials.Certificate('./assets/nurture-sync-99cb5fa4cc76.json')
        firebase_admin.initialize_app(cred)

# Call this function to initialize Firebase
initialize_firebase()

# Authentication functions here (sign_up_with_email_and_password, sign_in_with_email_and_password, etc.)


def sign_up_with_email_and_password(email, password, username=None):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        if username:
            payload["displayName"] = username 
        payload = json.dumps(payload)
        response = requests.post(rest_api_url, params={"key": "AIzaSyAWxDf2YbRpVpnfQr2ABLzf3zaAOe4mqfg"}, data=payload)
        return response.json()
    except Exception as e:
        return str(e)

def sign_in_with_email_and_password(email, password):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        payload = json.dumps(payload)
        response = requests.post(rest_api_url, params={"key": "AIzaSyAWxDf2YbRpVpnfQr2ABLzf3zaAOe4mqfg"}, data=payload)
        return response.json()
    except Exception as e:
        return str(e)

def reset_password(email):
    try:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
        payload = {
            "email": email,
            "requestType": "PASSWORD_RESET"
        }
        payload = json.dumps(payload)
        response = requests.post(rest_api_url, params={"key": "AIzaSyAWxDf2YbRpVpnfQr2ABLzf3zaAOe4mqfg"}, data=payload)
        if response.status_code == 200:
            return True, "Reset email sent"
        return False, response.json().get("error", {}).get("message", "Unknown error")
    except Exception as e:
        return False, str(e)
