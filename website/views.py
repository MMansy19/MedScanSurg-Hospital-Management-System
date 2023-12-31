from datetime import datetime
import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import *

views = Blueprint('views', __name__)

# Utility function to save a picture
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
        return 'default.jpg'

class EditProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=30)])
    password = StringField('Password', validators=[DataRequired(), Length(max=30)])
    specialty = StringField('Specialty', validators=[DataRequired(), Length(max=30)])
    salary = IntegerField('Salary', validators=[DataRequired()])
    working_hours = IntegerField('Working Hours', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    photo = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    def populate_from_doctor(self, doctor):
        self.full_name.data = doctor.full_name
        self.password.data = doctor.password
        self.specialty.data = doctor.specialty
        self.salary.data = doctor.salary
        self.working_hours.data = doctor.working_hours
        self.phone.data = doctor.phone
        self.address.data = doctor.address

    def update_doctor(self, doctor, photo_file):
        doctor.full_name = self.full_name.data
        doctor.password = self.password.data
        doctor.specialty = self.specialty.data
        doctor.salary = self.salary.data
        doctor.working_hours = self.working_hours.data
        doctor.phone = self.phone.data
        doctor.address = self.address.data

        if photo_file:
            doctor.photo = save_picture(photo_file)    


# Utility function to create a new patient
def create_patient(username, name, email, password, birthdate):
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    new_patient = Patient(username=username, name=name, email=email, password=password, birthdate=birthdate)
    db.session.add(new_patient)
    db.session.commit()

# Utility function to authenticate a user and render the appropriate template
def authenticate_user(user_type, username, password):
    if user_type == 'patient':
        user = Patient.query.filter_by(username=username).first()
    elif user_type == 'doctor':
        user = Doctor.query.filter_by(user_name=username).first()
    elif user_type == 'admin':
        if username == 'admin_username' and password == 'admin_password':
            return render_template('admin.html')

    if user and user.password == password:
        if user_type == 'patient':
            return render_template('index.html', patient=user)
            # return redirect(url_for('views.index', patient=user))
        elif user_type == 'doctor':
            # return render_template('doctor.html', doctor=user)
            return redirect(url_for('views.doctor', doctor_id=user.id))

    return None

# Utility function to create a new doctor
def create_doctor(ssn, email, password, user_name, full_name):
    existing_doctor = Doctor.query.filter_by(user_name=user_name).first()
    if not existing_doctor:
        new_doctor = Doctor(
            ssn=ssn, email=email, password=password, user_name=user_name,
            full_name=full_name, working_hours=40, salary=80000, phone='1234567890',
            address='Some Address', specialty='Surgery/Radiology'
        )
        db.session.add(new_doctor)
        db.session.commit()

# Utility function to handle appointment creation
def create_appointment(patient_id, doctor_id, appointment_time_str):
    appointment_time = datetime.strptime(appointment_time_str, '%Y-%m-%dT%H:%M')
    new_appointment = Appointment(doctor_id=doctor_id, patient_id=patient_id, appointment_time=appointment_time)
    db.session.add(new_appointment)
    db.session.commit()

# Main route for index
@views.route('/', methods=['GET', 'POST'])
@login_required
def index(patient_id):
    patient = Patient.query.get(patient_id)
    return render_template('index.html', patient=patient)

# Route for login
@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        check_create = 'create' in request.form
        check_sign = 'sign' in request.form

        if check_create:
            create_patient(
                request.form['username1'], request.form['fullname'],
                request.form['email'], request.form['password1'], request.form['birthdate']
            )
            return render_template('login.html')
     
        elif check_sign:
            user_type = request.form.get('userType')
            username = request.form.get('username2')
            password = request.form.get('password2')
            
            result_template = authenticate_user(user_type, username, password)
            if result_template:
                return result_template

    return render_template('login.html')

# Routes for doctor, patient, and admin
@views.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
def doctor(doctor_id):

    # Retrieve all appointments for the specified doctor with patient information
    appointments = (
        db.session.query(Appointment, Patient)
        .join(Patient, Appointment.patient_id == Patient.patient_id)
        .filter(Appointment.doctor_id == doctor_id)
        .all()
    )
    return render_template('doctor.html', appointments = appointments, doctor_id=doctor_id)

@views.route('/patient')
def patient():
    return render_template('patient.html')

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    doctors = Doctor.query.all()

    if request.method == 'POST':
        create_doctor(
            request.form['ssn'], request.form['email'], request.form['password'],
            request.form['user_name'], request.form['full_name']
        )

    return render_template('admin.html', doctors=doctors)

# Route for appointments
@views.route('/appointments/<int:patient_id>', methods=['GET', 'POST'])
def appointments(patient_id):
    if request.method == 'POST':
        create_appointment(
            patient_id, request.form.get('doctor_id'), request.form.get('appointment_time')
        )
        return redirect(url_for('views.appointments', patient_id=patient_id))

    doctors = Doctor.query.all()
    return render_template('appointments.html', doctors=doctors, patient_id=patient_id)

# Route for editing doctor profile
@views.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    form = EditProfileForm()

    if request.method == 'GET':
        form.populate_from_doctor(doctor)
        photo = url_for('static', filename=f'profile_pics/{doctor.photo}')
        return render_template('edit_doctor.html', photo=photo, form=form, doctor=doctor)

    form.update_doctor(doctor, request.files.get('photo'))
    db.session.commit()
    return redirect(url_for('views.admin'))

# Route for deleting a doctor
@views.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()

    for appointment in appointments:
        db.session.delete(appointment)

    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('views.admin'))

