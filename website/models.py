from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import the datetime module
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.exc import IntegrityError
import os
import secrets
from PIL import Image
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired, Length
from os import path
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for,jsonify
import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from . import  cursor, database_session
import psycopg2
import psycopg2.extras


views = Blueprint('views', __name__)

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
def create_patient(ssn,username, name, email, password, birthdate,photo):
    database_session.rollback()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
    photo: save_picture(photo)
    cursor.execute('INSERT INTO patient (ssn,user_name, full_name, email, password, birthdate, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)', (ssn,username, name, email, password, birthdate,photo))
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

def book_scan(scan_type,test_type,appointment_date,additional_notes,patient_id,time):
    message=None
    if scan_type:
        cursor.execute('SELECT date FROM surgery WHERE patient_id=%s', (patient_id,))
        surgery_registered_date=cursor.fetchall()
        surgery_registered_date = [str(item[0]) for item in surgery_registered_date]
        appointment_date=str(appointment_date)
        #####################################################
        cursor.execute('SELECT hour_minute FROM surgery WHERE patient_id=%s', (patient_id,))
        surgery_registered_hours=cursor.fetchall()
        surgery_registered_hours = [int(item[0].split(':')[0]) for item in surgery_registered_hours]
        # print(surgery_registered_hours)
        ##################################################
        cursor.execute('SELECT date FROM scan WHERE patient_id=%s', (patient_id,))
        scan_registered_date=cursor.fetchall()
        scan_registered_date = [str(item[0]) for item in scan_registered_date]
        cursor.execute('SELECT time FROM scan WHERE patient_id=%s', (patient_id,))
        scan_registered_hours=cursor.fetchall()
        scan_registered_hours = [int(item[0].split(':')[0]) if isinstance(item[0], str) else None for item in scan_registered_hours]
        
        time=int(time)
        if not any(time == registered_hour and appointment_date==date1  for registered_hour,date1 in zip(scan_registered_hours,scan_registered_date)):
            if not any(time == registered_hour and appointment_date==date1  for registered_hour,date1 in zip(surgery_registered_hours,surgery_registered_date)):
                if  scan_type :
                    if int(time)>=8 and int(time)<=18:
                        cursor.execute('INSERT INTO scan(machine,category,date,patient_notes,patient_id,time) VALUES (%s, %s,%s,%s,%s,%s)',(scan_type,test_type,appointment_date,additional_notes,patient_id,time) )
                        database_session.commit()
                        message='Scan is successefly registered'
                        return message
                    else:
                        message='Scaning department is closed at this time please choose time from 8 to 18'
                        return message
            else:
                message='You already registered a surgey at the same time'
                return message
        else:
            message='You already registered a scan at the same time'
            return message
        
def book_surgery(surgery_type,doctor_name,date,hour_minute,additional_notes,patient_id):
    message=None
    if surgery_type:
        doctor_name.split('.')
        # print(doctor_name)
        cursor.execute('SELECT id FROM doctor WHERE full_name = %s', (doctor_name,))
        id=int(cursor.fetchall()[0][0])
        ##########################
        cursor.execute('SELECT start_work FROM doctor WHERE full_name = %s', (doctor_name,))
        start_work=cursor.fetchall()[0][0]
        if start_work:
            int(start_work)
        cursor.execute('SELECT end_work FROM doctor WHERE full_name = %s', (doctor_name,))
        end_work=cursor.fetchall()[0][0]
        if end_work:
            int(start_work)
        
        ##########################
        
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
        #########################################
        cursor.execute('SELECT date FROM surgery WHERE patient_id=%s', (patient_id,))
        surgery_registered_date=cursor.fetchall()
        surgery_registered_date = [str(item[0]) for item in surgery_registered_date]
        #####################################################
        cursor.execute('SELECT hour_minute FROM surgery WHERE patient_id=%s', (patient_id,))
        surgery_registered_hours=cursor.fetchall()
        surgery_registered_hours = [int(item[0].split(':')[0]) for item in surgery_registered_hours]
        #########################################
        cursor.execute('SELECT date FROM scan WHERE patient_id=%s', (patient_id,))
        scan_registered_date=cursor.fetchall()
        scan_registered_date = [str(item[0]) for item in scan_registered_date]
        cursor.execute('SELECT time FROM scan WHERE patient_id=%s', (patient_id,))
        ################################################
        scan_registered_hours=cursor.fetchall()
        scan_registered_hours = [int(item[0].split(':')[0]) if isinstance(item[0], str) else None for item in scan_registered_hours]
        # print(hour)
        if start_work:
            if hour>=start_work and hour<=end_work:
                if not any(hour == registered_hour and date==date1  for registered_hour,date1 in zip(surgery_registered_hours,surgery_registered_date)):
                    if not any(hour == registered_hour and date==date1  for registered_hour,date1 in zip(scan_registered_hours,scan_registered_date)):
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
                    else:
                        message= 'You already registered a scan at the same time'
                        return message
                else:
                    message= 'You already registered a surgey at the same time'
                    return message
            else:
                message= 'Dr is only available between ' +str(start_work)+' and '+str(end_work)
                return message
                           
def get_doctor_by_id(doctor_id):
    database_session.rollback()
    cursor.execute('SELECT * FROM doctor WHERE ID = %s', (doctor_id,))
    return cursor.fetchone()
def get_patient_by_id(patient_id):
    database_session.rollback()
    cursor.execute('SELECT * FROM patient WHERE ID = %s', (patient_id,))
    return cursor.fetchone()

def get_scans_by_doctor_id(doctor_id):
    cursor.execute('SELECT * FROM Scan WHERE doctor_id = %s', (doctor_id,))
    return cursor.fetchall()

def get_unassigned_scans():
    cursor.execute('SELECT * FROM Scan WHERE doctor_id IS NULL')
    return cursor.fetchall()

def update_doctor_profile(doctor_id, data):
    cursor.execute('''
        UPDATE doctor
        SET full_name = %s, working_hours = %s, salary = %s, phone = %s, address = %s,
             photo = %s, start_work = %s, end_work = %s, department = %s
        WHERE ID = %s
    ''', (
        data['full_name'], data['working_hours'], data['salary'],
        data['phone'][:11] if data['phone'] else '', data['address'],
          data['photo'], data['start_work'], data['end_work'],data['department'], doctor_id
    ))
    database_session.commit()

def update_scan(doctor_id, data):
    cursor.execute('''
        UPDATE Scan
        SET price = %s, report = %s, doctor_id = %s
        WHERE scan_id = %s
    ''', (data['price'], data['report'], doctor_id, data['scan_id']))
    database_session.commit()

def delete_doctor(doctor_id):
    database_session.rollback()
    msg=None

    # Delete scans associated with the doctor
    cursor.execute('SELECT full_name FROM doctor WHERE id = %s', (doctor_id,))
    full_name=cursor.fetchone()
    cursor.execute('SELECT FROM scan WHERE doctor_id = %s', (doctor_id,))
    scan=cursor.fetchone()
    # Delete surgeries associated with the doctor
    cursor.execute('SELECT FROM surgery WHERE doctor_id = %s', (doctor_id,))
    surgery=cursor.fetchone()
    print(surgery)
    if len(scan)==0 or len(surgery)==0:
        msg=f"Can't Delete Dr.{full_name} as He  has Assigned to patient"
        return msg
    # Delete the doctor
    cursor.execute('DELETE FROM doctor WHERE id = %s', (doctor_id,))

    # Commit the changes to the database
    database_session.commit()

def create_doctor(data):
    database_session.rollback()
    cursor.execute('''
        INSERT INTO doctor (ssn, email, password, user_name, full_name,specialty, department, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        data['ssn'], data['email'], data['password'],
        data['user_name'], data['full_name'], data['specialty'], data['department'], data['gender']
    ))
    database_session.commit()

