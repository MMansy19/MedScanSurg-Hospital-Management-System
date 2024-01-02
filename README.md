# Radiology Department Database Project 🌐💻

This project is a Flask-based web application for managing a Radiology Department database. It allows users to login as patients, doctors, or administrators, schedule appointments, and manage user profiles.

## Project Overview

**MedRad Connect** is a comprehensive full-stack web application designed to cater to the unique needs of the Radiology Department. Developed using front-end technologies such as HTML, CSS, and JS, coupled with the Python Flask web micro framework, this project aims to provide a dynamic and responsive system. The application seamlessly integrates essential features of a Hospital Information System (HIS), specifically tailored for the Radiology Department.

## Table of Contents

- [Radiology Department Database Project 🌐💻](#radiology-department-database-project-)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [Running the Flask App](#-running-the-flask-app)
  - [Project Structure](#-project-structure)
  - [Editing a Doctor's Profile](#-editing-a-doctors-profile)
  - [Adding a New Doctor](#-adding-a-new-doctor)
  - [Managing Appointments](#-managing-appointments)
  - [Contact](#-contact)
  - [Video Presentation](#-video-presentation)

## 🚀 Running the Flask App

1. Open a terminal and navigate to the project directory:

   ```bash
   cd C:\Radiology-Department-Database-Project
   ```

2. If you don't have a virtual environment, create one:

   ```bash
   virtualenv venv
   ```

3. Activate the virtual environment:

   ```bash
   venv\Scripts\activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Flask app:

   ```bash
   python app.py
   ```

## 📂 Project Structure

- `website`: Contains the main Flask application.
  - `__init__.py`: Initializes the Flask app.
  - `models.py`: Defines the database models.
  - `views.py`: Contains the main views and routes.
  - ...

- `static`: Contains static files (CSS, JS, images).
  - `profile_pics`: Stores user profile pictures.

- `templates`: Contains HTML templates for rendering pages.
  - `admin.html`: Admin dashboard.
  - `appointments.html`: Appointments page.
  - `doctor.html`: Doctor dashboard.
  - `index.html`: Home page.
  - `login.html`: Login and registration page.
  - `patient.html`: Patient dashboard.
  - ...

- `instance`: Contains instance-specific configuration files.

- `database.db`: SQLite database file.

- `ER_model.jpg`: Entity-Relationship model image.

- `Planning`: Directory containing planning documents.

## ✏️ Editing a Doctor's Profile

To edit a doctor's profile, visit the `/edit_doctor/<doctor_id>` route. The admin can manage doctors' information, including their profile pictures.

## ➕ Adding a New Doctor

To add a new doctor, go to the `/admin` route and fill in the required information in the form.

## 📅 Managing Appointments

Patients can schedule appointments by visiting the `/appointments/<patient_id>` route. Doctors and administrators can view and manage appointments.

## 📧 Contact

For inquiries or issues, please contact [Mahmoud Mansy] at [mmansy@egmail.com].

## 🎥 Video Presentation

[![Radiology Department Database Project Presentation](./images/video_thumbnail.png)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
