import streamlit as st
import firebase_admin
from firebase_admin import credentials, db, get_app, initialize_app
from datetime import datetime
import json
import requests
import uuid
import os
from io import BytesIO


def download_file(url, destination_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded successfully to {destination_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")

# Example usage
url = 'https://raw.githubusercontent.com/PrasadKhambadkar/Navigation_Feedback_Form/main/sih-1710-cc98c04cdbab.json'
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
    cred = credentials.Certificate(url)
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
    st.error("Bot detection triggered. Please do not submit the form with modifications to hidden fields.")
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
