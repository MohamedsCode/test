import streamlit as st
import pandas as pd


# Function to get doctors for the patient to book appointments
def get_available_doctors():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors WHERE availability = 'available'")
    doctors = cursor.fetchall()
    conn.close()
    return doctors

# Function for admin to add a new patient
def add_patient(username, password, name, age, gender):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (username, password, name, age, gender) VALUES (%s, %s, %s, %s, %s)", (username, password, name, age, gender))
    conn.commit()
    conn.close()

# Function for doctors to toggle availability
def toggle_availability(doctor_id, availability):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE doctors SET availability = %s WHERE id = %s", (availability, doctor_id))
    conn.commit()
    conn.close()

# Function to display the login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
        else:
            st.error("Invalid username or password")

# Function to display patient dashboard
def patient_dashboard():
    st.title(f"Welcome {st.session_state.user['name']} (Patient)")

    # Show patient's medical history
    st.subheader("Medical History")
    st.write("Display medical history here...")

    # Appointment booking
    st.subheader("Book Appointment")
    doctors = get_available_doctors()
    if doctors:
        doctor_choices = [f"{doctor['name']} ({doctor['specialty']})" for doctor in doctors]
        selected_doctor = st.selectbox("Choose a Doctor", doctor_choices)
        if st.button("Book Appointment"):
            st.success(f"Appointment booked with {selected_doctor}")
    else:
        st.warning("No doctors available right now.")

# Function to display doctor dashboard
def doctor_dashboard():
    st.title(f"Welcome {st.session_state.user['name']} (Doctor)")

    # Toggle doctor availability
    st.subheader("Set Availability")
    availability = st.radio("Availability", ("available", "not available"))
    if st.button("Update Availability"):
        toggle_availability(st.session_state.user['id'], availability)
        st.success("Availability updated!")

    # View appointments booked with the doctor
    st.subheader("Appointments")
    st.write("List of appointments booked with the doctor will go here...")

# Function to display admin dashboard
def admin_dashboard():
    st.title(f"Welcome {st.session_state.user['name']} (Admin)")

    # Add a new patient
    st.subheader("Add New Patient")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    if st.button("Add Patient"):
        add_patient(username, password, name, age, gender)
        st.success(f"Patient {name} added successfully!")

# Main function to control login and user roles
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if not st.session_state.logged_in:
        login_page()
    else:
        user = st.session_state.user
        if user['role'] == 'patient':
            patient_dashboard()
        elif user['role'] == 'doctor':
            doctor_dashboard()
        elif user['role'] == 'admin':
            admin_dashboard()

if __name__ == "__main__":
    main()
