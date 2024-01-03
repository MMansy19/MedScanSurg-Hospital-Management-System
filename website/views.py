from datetime import datetime
import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from flask_login import login_required, current_user
from . import db , cursor
from .models import *
import psycopg2
import psycopg2.extras

views = Blueprint('views', __name__)

database_session = psycopg2.connect(
    database='postgres',
    port=5432,
    host='localhost',
    user='postgres',
    password= 'admin'
)
cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
def save_scan(form_picture):
    if form_picture and form_picture.filename:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(views.root_path, 'static/scans', picture_fn)

        output_size = (300, 300)  # Adjust the size as needed
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn
    else:
        return 'default.jpg'


# Utility function to create a new patient
def create_patient(username, name, email, password, birthdate):
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    cursor.execute('INSERT INTO patient (user_name, full_name, email, password, birthdate) VALUES (%s, %s, %s, %s, %s)', (username, name, email, password, birthdate))
    database_session.commit()
# Utility function to authenticate a user and render the appropriate template
def authenticate_user(user_type, username, password):
    if user_type == 'patient':
                cursor.execute('SELECT * FROM patient WHERE user_name = %s', (username,))
                patient = cursor.fetchone()
                print(patient[4])
                if patient[4] is not None:
                    if patient[4] == password:
                     return redirect(url_for('views.patient',patient_id = patient[0]))

    elif user_type == 'doctor':
        cursor.execute('SELECT * FROM doctor WHERE user_name = %s', (username,))
        doctor = cursor.fetchone()
        if doctor:
            if doctor[4] ==  password:
                return redirect(url_for('views.doctor', doctor_id = doctor[0]))
    
    elif user_type == 'admin':
        if username == 'admin_username' and password == 'admin_password':
            return render_template('admin.html')

    return render_template('login.html')

# Utility function to create a new doctor
def create_doctor(ssn, email, password, user_name, full_name):
        cursor.execute('SELECT * FROM doctor WHERE user_name = %s', (user_name,))
        existing_doctor=cursor.fetchone()
        
        if not existing_doctor:
            working_hours = 40
            salary = 80000
            phone = '1234567890'
            address = 'Some Address'
            specialty= 'Neurosurgery'
            gender='M' 
            cursor.execute('INSERT INTO doctor(ssn,email, password, user_name,full_name,working_hours,salary,phone,address,specialty,gender) VALUES (%s, %s ,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (ssn,email,password, user_name, full_name,working_hours,salary,phone,address, specialty,gender))
            database_session.commit()

# Utility function to handle appointment creation
# def create_appointment(patient_id, doctor_id, appointment_time_str):
#     appointment_time = datetime.strptime(appointment_time_str, '%Y-%m-%dT%H:%M')
#     new_appointment = Appointment(doctor_id=doctor_id, patient_id=patient_id, appointment_time=appointment_time)
#     db.session.add(new_appointment)
#     db.session.commit()

# Main route for index
@views.route('/', methods=['GET', 'POST'])

def index():
    return render_template('index.html')

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

    # cursor.execute(f'SELECT scan.*, patient.* FROM appointment JOIN patient ON scan.patient_id = patient.ID WHERE scan.doctor_id = %s',(doctor_id),)
    # appointments = cursor.fetchall()

@views.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
def doctor(doctor_id):
    database_session.rollback()
    # Fetch the doctor's information for rendering the form
    cursor.execute('SELECT * FROM doctor WHERE ID = %s', (doctor_id,))
    doctor = cursor.fetchone()
    
    cursor.execute('SELECT * FROM Scan')
    scan = cursor.fetchall()

    if request.method == 'POST':
    
        full_name = request.form.get('full_name')
        full_name = request.form.get('full_name')
        working_hours = int(request.form.get('working_hours')) if request.form.get('working_hours') else 0
        salary = int(request.form.get('salary')) if request.form.get('salary') else 0
        phone = request.form.get('phone')[:11] if request.form.get('phone') else ''
        address = request.form.get('address')
        specialty = request.form.get('specialty')
        gender = request.form.get('gender')

        new_photo = request.files.get('photo')
        photo = save_picture(new_photo)
                
        # Update the doctor's profile in the database
        cursor.execute('''
            UPDATE doctor
            SET full_name = %s, working_hours = %s, salary = %s, phone = %s, address = %s,
                specialty = %s, gender = %s, photo = %s
            WHERE ID = %s
        ''', (full_name, working_hours, salary, phone, address, specialty, gender, photo, doctor_id))
        database_session.commit()
        
         # Fetch the scans from the form
        price = int(request.form.get('price')) if request.form.get('price') else 0
        new_scan_photo = request.files.get('report')
        scan_photo = save_scan(new_scan_photo)
                
        cursor.execute('''
            UPDATE Scan
            SET price = %s, report = %s, doctor_id = %s
            WHERE scan_id = %s
        ''', (price, scan_photo, doctor_id ,scan[3][0] ))
        database_session.commit()

        return redirect(url_for('views.doctor', doctor_id=doctor_id))

    # # Rollback the current transaction
    # database_session.rollback()
    
    # # Fetch the doctor's information for rendering the form
    # cursor.execute('SELECT * FROM doctor WHERE ID = %s', (doctor_id,))
    # doctor = cursor.fetchone()
    
    # cursor.execute('SELECT * FROM Scan WHERE doctor_id = %s', (doctor_id,))
    # scans = cursor.fetchall()

    return render_template('doctor.html', doctor=doctor, scan=scan)

@views.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient(patient_id):
    message=None
    message1=None
    if  request.method == 'POST':
        scan_type = request.form.get('scanType')
        # print(scan_type)
        test_type = request.form.get('testType')
        appointment_date = request.form.get('appointmentDate')
        additional_notes = request.form.get('additionalNotes')
        hour_minute1 = request.form.get('appointmentHour1')
        message1= book_scan(scan_type,test_type,appointment_date,additional_notes,patient_id,hour_minute1)
        surgery_type = request.form.get('SurgeryType')
        doctor_name = request.form.get('DoctorName')
        date = request.form.get('appointmentDate2')
        hour_minute = request.form.get('appointmentHour')
        patient_notes = request.form.get('additionalNotes2')
        # print(hour_minute)
        # print(type(date))     
        message=book_surgery(surgery_type,doctor_name,date,hour_minute,patient_notes,patient_id)
    cursor.execute('SELECT * FROM patient WHERE ID = %s', (patient_id,))
    patient = cursor.fetchone()
    cursor.execute('SELECT * FROM surgery WHERE patient_id = %s', (patient_id,))
    surgerys=cursor.fetchall()
    cursor.execute('SELECT * FROM scan WHERE patient_id = %s', (patient_id,))
    scans=cursor.fetchall()
    cursor.execute('SELECT * FROM doctor')
    options=cursor.fetchall()
    return render_template('patient.html',patient=patient,surgerys=surgerys,scans=scans,msg=message,msg1=message1,options=options)

@views.route('/get_doctors', methods=['POST'])
def get_doctors():
    cursor.execute('SELECT * FROM doctor')
    doctors_data=cursor.fetchall()
    surgery_type = request.form.get('SurgeryType')
    filtered_doctors = [doctor for doctor in doctors_data if doctor[11] == surgery_type]
    return jsonify(filtered_doctors)

def book_scan(scan_type,test_type,appointment_date,additional_notes,patient_id,time):
    message=None
    if  scan_type :
        # appointment_day=(appointment_date.split('-')[-1])
        # appointment_month=(appointment_date.split('-')[-2])
        # appointment_year=(appointment_date.split('-')[-3])
        if int(time)>=8 and int(time)<=18:
            cursor.execute('INSERT INTO scan(machine,category,date,patient_notes,patient_id,time) VALUES (%s, %s,%s,%s,%s,%s)',(scan_type,test_type,appointment_date,additional_notes,patient_id,time) )
            database_session.commit()
            message='Scan is successefly registered'
            return message
        else:
            message='Scaning department is closed at this time please choose time from 8 to 18'
            return message
        
def book_surgery(surgery_type,doctor_name,date,hour_minute,additional_notes,patient_id):
    message=None
    if surgery_type:
        doctor_name.split('.')
        # print(doctor_name)
        cursor.execute('SELECT id FROM doctor WHERE full_name = %s', (doctor_name,))
        id=int(cursor.fetchall()[0][0])
        # print(id)
        cursor.execute('SELECT hour_minute FROM surgery WHERE doctor_id=%s', (id,))
        doctor_registered_hours=cursor.fetchall()
        doctor_registered_hours = [int(item[0]) for item in doctor_registered_hours]
        ###########################
        cursor.execute('SELECT date FROM surgery WHERE doctor_id=%s', (id,))
        doctor_registered_date=cursor.fetchall()
        doctor_registered_date = [str(item[0]) for item in doctor_registered_date]
        print(doctor_registered_date)
        hour=int(hour_minute)
        # print(hour)
        if not any(hour == registered_hour and date==date1  for registered_hour,date1 in zip(doctor_registered_hours,doctor_registered_date)):
            if  id:              ##untill doctor is linked to patient then remove not
                cursor.execute('INSERT INTO surgery(type,date,hour_minute,additional_notes,patient_id,doctor_name,doctor_id) VALUES (%s, %s,%s,%s,%s,%s,%s)',(surgery_type,date,hour_minute,additional_notes,patient_id,doctor_name,id) )
                database_session.commit()   
                message='Surgery is successfuly registered with'+' '+'Dr '+doctor_name
                return message
        else:
            print('hour is out of range')
            message= 'Dr '+doctor_name+' '+ 'is not available at this time'
            return message

@views.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':
        create_doctor(
            request.form['ssn'], request.form['email'], request.form['password'],
            request.form['user_name'], request.form['full_name']
        )

    cursor.execute('SELECT * FROM doctor')
    doctors = cursor.fetchall()
    return render_template('admin.html', doctors=doctors)

@views.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    database_session.rollback()
    cursor.execute('SELECT * FROM doctor WHERE id = %s', (doctor_id,))
    doctor=cursor.fetchone()

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        working_hours = int(request.form.get('working_hours')) if request.form.get('working_hours') else 0
        salary = int(request.form.get('salary')) if request.form.get('salary') else 0
        phone = request.form.get('phone')[:11] if request.form.get('phone') else ''
        address = request.form.get('address')
        specialty = request.form.get('specialty')
        gender = request.form.get('gender')

        new_photo = request.files.get('photo')
        photo = save_picture(new_photo)

        # Update the doctor's profile in the database
        cursor.execute('''
            UPDATE doctor
            SET full_name = %s, working_hours = %s, salary = %s, phone = %s, address = %s,
                specialty = %s, gender = %s, photo = %s
            WHERE ID = %s
        ''', (full_name, working_hours, salary, phone, address, specialty, gender, photo, doctor_id))
        database_session.commit()
        
    return render_template('edit_doctor.html', doctor=doctor)

# Route for deleting a doctor
@views.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    cursor.execute('DELETE FROM doctor WHERE id = %s', (doctor_id,))
    database_session.commit()
    return redirect(url_for('views.admin'))


