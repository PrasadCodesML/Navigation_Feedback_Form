import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, get_app, initialize_app
from datetime import datetime
import json
import requests
import uuid
import os
from io import BytesIO


firebase_creds = {
  "type": "service_account",
  "project_id": "sih-1710",
  "private_key_id": "cc98c04cdbab6a9b0e75f3cdbd92024636c6aeb5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDkpvaSxSqvyF75\nNzvrg+CSFnxYs/GTWibtItrS0CxWLKkVOEXP65zGWgSHeYbSblEe9XOh1RBV17Fp\nK3UNLlcYWgmgBJYMGY0qVQc/R8KLGrur7sivGHt44VLV7hkw1T2QdWsnuAwpmD7N\nSEiLEFt0VrEZayCaLnHdLhiJDlP5MwBBnTT8hjuXefVi5Lhwknr/tRCrGh0kdmQu\nBs94rZ50WJJot/muDGgiCl7cqzidg7CycAJmkQgrOdt1pnmBZ4l2iIdf4gajSq3S\nkt1WtiIx1pj7ODT7JTykLilm1XBaZdTxTd1Veq0N0IWSFbsCtIbGovgIZz+mYIbY\nNPJthzMdAgMBAAECggEANiGV6djOOofV/iuWnrLdqVAz938AP8l9wjG4euSoPm17\nyQeFtYva1XWNsXHymmJeB5WF3sf1glEaUeLlJu3z1hLIyQ6U5D/vVNiE6vUG6E43\npGRXM+a4on07kmR4J8Cv/sFhkSloDbfalFhavjts302/xxv+v6mjsMB/NAFFnY7D\n9XgO6CbCMc5KNEfBYIdqT7r8agSAZfbs1zT0lvARB/LC4GDpaT68UUKeGI/y8s1z\ngxP64bPok7KRKjycj+YU+J9qPhLBbVxXNvvfwha+OLq1P6uIUMwMmwxiLVeVHx9D\nC+8FfSuDgKl4DBJAq8DwUJgecZw/y2psC5tRE7TAMQKBgQD/XpionhcyXClFEHvr\nRQmH91cad6THVD+tO/4ctiKP9I802ZnZtr9QMtL1qaNQUFX1g3e9JHxQo8zlBT6G\ncuG8J2ehKT/lBsT1NU6DNznz8PZmSusgLaU2P9GdLzjSMM3DP5E4+/6BAeRFWAAc\nsuDDyKlIVDIlIh1LvVmFHYDKUQKBgQDlN3r+r1izrb4CNr97JgToTitHqCSS4DnF\nNAuQeqJSbuCrmvnxrmTZIsrFDi+V2wi1XvOeRJaXWjrkUTM/et3p4BLfWYKQF8Fy\nBb0eeOw441fY7EpCkFqNGpQKmTzFQW8lhy66SHLonNvAbSFTQPJUq0ui9lTqvQ07\nQt0IX8XdDQKBgQDBodvFNyJFqEYOvUIJEe75Lt3YDtJd5g7mby/uW1h3qSuRGlIj\nGAOWbwMxDTDtLA0RvV7khy7QAnPRUBmp3qA1h/d25w0wvuJHP+VJb228/4AF7la8\nrn+wU9HACtdd4W2T17Zo7AJ9lY6d2e0z1ZrCOXvKgTUInQZzsJ6ZZdaLEQKBgGBs\nS1gyCR1kvCaQQ1KZtrzGjVxSdjg3DPZRI4A+pmQI8ogd5IDvfMr+4M+uXQQsJOiv\nLcppTfQTZ+y939IXbJzCvw2nyM22wJCnq1vTQIPZ1w2QsNh5gy4SfS5MMg1Erm3a\nBSUl7vi9a4/yGG++RXKqsGG4QBaTOqqwQO0R5NlNAoGBAMh3z172mUMImi6mJLnQ\nizJI5uWMO9wg/++8HPdP+NZ2skV90YyIUgiWyJZ4aFEqj+83Igi55ZmsFlp19TN0\nnV5Z4m2/pacWWg3KvslZT87CZ7KaOp+Q7V4oHMQeUnqkBgrRljcBdqcvPCzGFTaY\nFGp4qvdyJ3gqwb9KiTyNYJlY\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-2e7ck@sih-1710.iam.gserviceaccount.com",
  "client_id": "106069457853857224746",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2e7ck%40sih-1710.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
def get_location():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    loc = data['loc'].split(',')
    latitude = float(loc[0])
    longitude = float(loc[1])
    return latitude, longitude


try:
    app = get_app()
except ValueError:
    cred = credentials.Certificate(firebase_creds)
    app = initialize_app(cred, {
        'databaseURL': 'https://sih-1710-default-rtdb.firebaseio.com/',
    })
# Reference to the Firebase Realtime Database
ref = db.reference('feedback')

# Streamlit form for feedback
st.title("Navigation System Feedback Form")

hidden_field = st.text_input("Enter your City", label_visibility="hidden", disabled=True)

# Check if the hidden field was filled out
if hidden_field:
    st.error("Bot detected.")
else:
    user_name = st.text_input("User Name")
    user_email = st.text_input("Email")
    navigation_errors = {
        "Incorrect starting position": st.checkbox("Incorrect starting position"),
        "Incorrect destination position": st.checkbox("Incorrect destination position"),
        "Route not available": st.checkbox("Route not available"),
        "Navigation took longer than expected": st.checkbox("Navigation took longer than expected"),
        "Lost GPS signal": st.checkbox("Lost GPS signal"),
        "Incorrect turn instructions": st.checkbox("Incorrect turn instructions"),
        "Route recalculated unnecessarily": st.checkbox("Route recalculated unnecessarily"),
        "Navigation stopped unexpectedly": st.checkbox("Navigation stopped unexpectedly"),
        "Others": st.checkbox("Others")
    }
    other_error_description = ""
    if navigation_errors["Others"]:
        other_error_description = st.text_area("Please describe the other error(s)")
    wrong_coordinates = st.text_input("Enter Wrong Latitude, Longitude")
    right_coordinates = st.text_input("Enter Correct Latitude, Longitude")
    start_position = st.text_input("Starting Position (Name the position on the Station where you started)")
    destination_position = st.text_input("Destination Position (Name the position of the Destination)")
    error_description = st.text_area("Describe the error")

    if st.button("Submit Feedback"):
        # Gather selected errors
        selected_errors = [error for error, selected in navigation_errors.items() if selected]
        latitude, longitude = get_location()

        # Prepare the feedback data
        feedback_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': user_name,
            'user_email': user_email,
            'error_description': error_description,
            'navigation_errors': selected_errors,
            'other_error_description': other_error_description,
            'wrong_coordinates': wrong_coordinates,
            'right_coordinates': right_coordinates,
            'start_position': start_position,
            'destination_position': destination_position,
            'current_lat': latitude,
            'current_long': longitude
        }

        # Push the feedback to Firebase Realtime Database
        ref.push(feedback_data)
        
        st.success("Thank you for your feedback!")
