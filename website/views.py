from datetime import datetime
import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for
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
    password= 'root1234'
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

        output_size = (500, 500)  # Adjust the size as needed
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
            return render_template('admin2.html')

    return render_template('login.html')

# Utility function to create a new doctor
def create_doctor(ssn, email, password, user_name, full_name,department,Gender):
        cursor.execute('SELECT * FROM doctor WHERE user_name = %s', (user_name,))
        existing_doctor=cursor.fetchone()
        
        if not existing_doctor:
            working_hours = 40
            salary = 80000
            phone = '1234567890'
            address = 'Some Address'
            specialty= department
            gender= Gender[0]
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
    # cursor.execute(f'SELECT * FROM patient WHERE ID = {patient_id};')
    # patient = cursor.fetchone()
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
    
    cursor.execute('SELECT * FROM Scan WHERE doctor_id IS NOT NULL')
    scans = cursor.fetchall()
    
    cursor.execute('SELECT * FROM Scan WHERE doctor_id IS NULL')
    scans2 = cursor.fetchall()
    
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
        
        
        price = int(request.form.get('price')) if request.form.get('price') else 0
        new_scan_photo = request.files.get('report')
        scan_photo = save_scan(new_scan_photo)
        scan_id = int(request.form.get('scan_id'))  # Fetch the scan_id from the form

        cursor.execute('''
            UPDATE Scan
            SET price = %s, report = %s, doctor_id = %s
            WHERE scan_id = %s
        ''', (price, scan_photo, doctor_id, scan_id))
        database_session.commit()

        return redirect(url_for('views.doctor', doctor_id=doctor_id))
    

    # if doctor[10] == 'Radiology':
    # return render_template('Radiologydoctor.html', doctor=doctor, scans=scans, scans2=scans2)
    
    # elif doctor[10] == 'Surgery':
    return render_template('Surgerydoctor.html', doctor=doctor, scans=scans, scans2=scans2)
 
    # return render_template('doctor.html', doctor=doctor, scans=scans, scans2=scans2)

@views.route('/scan_detail/<int:scan_id>')
def scan_detail(scan_id):
    cursor.execute('SELECT * FROM scan WHERE scan_id = %s', (scan_id,))
    scan = cursor.fetchone()

    return render_template('scan_detail.html', scan_id=scan_id, scan=scan)

@views.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient(patient_id):
    message=None
    if  request.method == 'POST':
        scan_type = request.form.get('scanType')
        print(scan_type)
        test_type = request.form.get('testType')
        appointment_date = request.form.get('appointmentDate')
        additional_notes = request.form.get('additionalNotes')
        hour_minute1 = request.form.get('appointmentHour')
        book_scan(scan_type,test_type,appointment_date,additional_notes,patient_id,hour_minute1)
      
        surgery_type = request.form.get('SurgeryType')
        doctor_name = request.form.get('DoctorName')
        date = request.form.get('appointmentDate2')
        hour_minute = request.form.get('appointmentHour')
        patient_notes = request.form.get('additionalNotes2')
        print(hour_minute)
        message=book_surgery(surgery_type,doctor_name,date,hour_minute,additional_notes,patient_id)
    cursor.execute('SELECT * FROM patient WHERE ID = %s', (patient_id,))
    patient = cursor.fetchone()
    cursor.execute('SELECT * FROM surgery WHERE patient_id = %s', (patient_id,))
    surgerys=cursor.fetchall()
    cursor.execute('SELECT * FROM scan WHERE patient_id = %s', (patient_id,))
    scans=cursor.fetchall()
    return render_template('patient.html',patient=patient,surgerys=surgerys,scans=scans,msg=message)

@views.route('/view_patient_info/<int:patient_id>')
def view_patient_info(patient_id):
    # Fetch patient information from the database
    cursor.execute('SELECT * FROM Patient WHERE ID = %s', (patient_id,))
    patient_info = cursor.fetchone()

    return render_template('view_patient_info.html', patient_info=patient_info)

def book_scan(scan_type,test_type,appointment_date,additional_notes,patient_id,time):
    if  scan_type :
        appointment_day=(appointment_date.split('-')[-1])
        appointment_month=(appointment_date.split('-')[-2])
        appointment_year=(appointment_date.split('-')[-3])
        cursor.execute('INSERT INTO scan(machine,category,date,patient_notes,patient_id,time) VALUES (%s, %s,%s,%s,%s,%s)',(scan_type,test_type,appointment_date,additional_notes,patient_id,time) )
        database_session.commit()
        
def book_surgery(surgery_type,doctor_name,date,hour_minute,additional_notes,patient_id):
    message=None
    if surgery_type:
        cursor.execute('SELECT id FROM doctor WHERE full_name = %s', (doctor_name,))
        id=cursor.fetchall()
        print(id)
        print(doctor_name)
        hour=int(hour_minute.split(':')[0])
        print(hour)
        if hour<=16 and hour>=8:
            if not id:              ##untill doctor is linked to patient then remove not
                cursor.execute('INSERT INTO surgery(type,date,hour_minute,additional_notes,patient_id,doctor_name) VALUES (%s, %s,%s,%s,%s,%s)',(surgery_type,date,hour_minute,additional_notes,patient_id,doctor_name) )
                database_session.commit()   
                message='Surgery is successfuly registered with'+' '+doctor_name
                return message
            else:  
                print('doctor id is none')
        else:
            print('hour is out of range')
            message= doctor_name+' '+ 'is busy at this time'
            return message

def admin():

    if request.method == 'POST':
        create_doctor(
            request.form['ssn'], request.form['email'], request.form['password'],
            request.form['user_name'], request.form['full_name'], request.form['department'], request.form['Gender']
        )

    cursor.execute('SELECT * FROM doctor')
    doctors = cursor.fetchall()
    doctors_count = len(doctors)

    cursor.execute('SELECT * FROM patient')
    patients = cursor.fetchall()
    patients_count = len(patients)

    cursor.execute('SELECT * FROM scan')
    scans = cursor.fetchall()
    scans_count = len(scans)

    cursor.execute('SELECT * FROM surgery')
    surgeries = cursor.fetchall()
    surgery_count = len(surgeries)

    app_count = scans_count+surgery_count

    return render_template('admin2.html', doctors=doctors,doctors_count=doctors_count,
                           patient_count=patients_count,app_count=app_count)

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

