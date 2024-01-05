# 𝐌𝐞𝐝𝐒𝐜𝐚𝐧𝐒𝐮𝐫𝐠 𝐂𝐨𝐧𝐧𝐞𝐜𝐭 🌐💻
-MedScanSurg Connect streamlines and empowers patients, providing a user-friendly portal for scheduling scans, radiology appointments, and surgeries, fostering efficient healthcare access and choices.
-This project is a Flask-based web application for managing a Radiology Department database. It allows users to login as patients, doctors, or administrators, schedule appointments, and manage user profiles.

## 🎥 [Video Presentation](https://drive.google.com/file/d/1XUMfUSOsbVn4jWmsddq0c2hgfBW1Q-fT/view?usp=sharing)

## Project Overview
**MedRad Connect** is a comprehensive full-stack web application designed to cater to the unique needs of the Radiology Department. Developed using front-end technologies such as HTML, CSS, and JS, coupled with the Python Flask web micro framework, this project aims to provide a dynamic and responsive system. The application seamlessly integrates essential features of a Hospital Information System (HIS), specifically tailored for the Radiology Department.


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

