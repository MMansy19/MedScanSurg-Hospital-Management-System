from . import db
from .models import *

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from flask_login import  login_required, current_user
import os
import secrets
from PIL import Image


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def index(patient_id):
    patient = Patient.query.get(patient_id)

    return render_template('index.html', patient=patient)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        check_create = 'create' in request.form  
        check_sign = 'sign' in request.form

        if check_create:
            username1 = request.form['username1']
            name1 = request.form['fullname']
            email = request.form['email']
            password1 = request.form['password1']
            birthdate = request.form['birthdate']
            # Convert birthdate string to a date object
            birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()

            # Create a new patient
            new_patient = Patient(username=username1, name=name1, email=email, password=password1, birthdate=birthdate)

            db.session.add(new_patient)
            db.session.commit()
            
            return render_template('login.html')
        elif check_sign:
            user_type = request.form.get('userType')
            username2 = request.form.get('username2')
            password2 = request.form.get('password2')
        
            if(user_type)=='patient':
                patient = Patient.query.filter_by(username=username2).first()
                if patient:
                    if patient.password ==  password2:
                        return render_template('index.html', patient = patient)
                    
            elif(user_type)=='doctor':
                doctor = Doctor.query.filter_by(user_name=username2).first()
                if doctor:
                    if doctor.password ==  password2:
                        return render_template('doctor.html', doctor=doctor)
                    
            elif(user_type)=='admin':
                #this is admin password and admin username
                if  password2==  'admin_password' and username2 == 'admin_username': 
                    return render_template('admin.html')
    # Render the login form for GET requests
    return render_template('login.html')

@views.route('/doctor')
def doctor():
    return render_template('doctor.html')

@views.route('/patient')
def patient():
    return render_template('patient.html')

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    doctors = Doctor.query.all()
    if request.method == 'POST':

        # Get form data
        ssn = request.form['ssn']
        email = request.form['email']
        password = request.form['password']
        user_name = request.form['user_name']
        full_name = request.form['full_name']

      # Check if the user_name already exists
        existing_doctor = Doctor.query.filter_by(user_name=user_name).first()
       
        if not existing_doctor:
            
            # Create a new doctor
            new_doctor = Doctor(ssn=ssn, email=email, password=password, user_name=user_name,
                                full_name=full_name, working_hours=40, salary=80000, phone='1234567890', address='Some Address',specialty='Surgery/Radiology' )

            # Add the doctor to the database
            db.session.add(new_doctor)
            
            db.session.commit()

    
    return render_template('admin.html', doctors=doctors )

@views.route('/appointments/<int:patient_id>', methods=['GET', 'POST'])
def appointments(patient_id):
    if request.method == 'POST':
        # Handle appointment creation
        doctor_id = request.form.get('doctor_id')
        patient = Patient.query.get(patient_id)


        # Check if the appointment time is available (you can add validation logic here)

        new_appointment = Appointment(doctor_id=doctor_id, patient_id=patient.patient_id)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('views.appointments',patient_id=patient_id))

    # Fetch all doctors and pass them to the template
    doctors = Doctor.query.all()
    return render_template('appointments.html', doctors = doctors, patient_id = patient_id )


@views.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    # Find the doctor in the database
    doctor = Doctor.query.get(doctor_id)

    form = EditProfileForm()
    if request.method == 'GET':
        # Populate the form with current doctor information
        form.password.data = doctor.password
        form.full_name.data = doctor.full_name
        form.working_hours.data = doctor.working_hours
        form.salary.data = doctor.salary
        form.specialty.data = doctor.specialty
        form.phone.data = doctor.phone
        form.address.data = doctor.address

        # You may need to adjust the following line based on your file structure
        photo = url_for('static', filename=f'profile_pics/{doctor.photo}')
        return render_template('edit_doctor.html', photo=photo, form=form, doctor=doctor)


    doctor.password = form.password.data
    doctor.full_name = form.full_name.data
    doctor.specialty=form.specialty.data
    doctor.phone=form.phone.data 
    doctor.working_hours = form.working_hours.data
    doctor.salary = form.salary.data
    doctor.address = form.address.data

    if form.photo.data:
        photo = save_picture(request.files['photo'])
        doctor.photo = photo

    db.session.commit()
    return redirect(url_for('views.admin'))  # Change 'admin' to your desired endpoint


@views.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    # Find the doctor in the database
    doctor = Doctor.query.get(doctor_id)
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    for appointment in appointments:
        db.session.delete(appointment)
    db.session.delete(doctor)
    db.session.commit()

    return redirect(url_for('views.admin'))

def save_picture(form_picture):
    if form_picture and form_picture.filename:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(views.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn
    else:
        return 'default.jpg'  # or any default image filename you want to use
