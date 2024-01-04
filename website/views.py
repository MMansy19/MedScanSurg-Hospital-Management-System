from flask import render_template, redirect, url_for, request, jsonify
from .models import *


@views.route('/', methods=['GET', 'POST'])
def index():
    database_session.rollback()
    return render_template('index.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    
    database_session.rollback()
    if request.method == 'POST':
        check_create = 'create' in request.form
        check_sign = 'sign' in request.form
        photo: save_picture(request.files.get('photo'))

        if check_create:
            create_patient(request.form['ssn'], request.form['username1'], request.form['fullname'],
                            request.form['email'], request.form['password1'], request.form['birthdate'], request.form['photo'])
            return render_template('login.html')
     
        elif check_sign:
            user_type = request.form.get('userType')
            username = request.form.get('username2')
            password = request.form.get('password2')
            
            result_template = authenticate_user(user_type, username, password)
            if result_template:
                return result_template

    return render_template('login.html')

@views.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
def doctor(doctor_id):
    database_session.rollback()
  
    doctor = get_doctor_by_id(doctor_id)
    scans = get_scans_by_doctor_id(doctor_id)
    scans2 = get_unassigned_scans()
    cursor.execute('SELECT * FROM surgery WHERE doctor_id = %s', (doctor_id,))
    surgerys=cursor.fetchall()   
    if request.method == 'POST':

        scan_data = {
            'price': int(request.form.get('price')) if request.form.get('price') else 0,
            'report': save_scan(request.files.get('report')),
            'scan_id': int(request.form.get('scan_id'))
        }

        update_scan(doctor_id, scan_data)

        return redirect(url_for('views.doctor', doctor_id=doctor_id))
        
    if doctor['department'] == 'Radiology':
        return render_template('Radiologydoctor.html', doctor=doctor, scans=scans, scans2=scans2)
    if doctor['department'] == 'Surgery':
        return render_template('Surgerydoctor.html', doctor=doctor,surgerys=surgerys)
    
    return render_template('Radiologydoctor.html', doctor=doctor, scans=scans, scans2=scans2)

@views.route('/scan_detail/<int:scan_id>')
def scan_detail(scan_id):
    database_session.rollback()
    cursor.execute('SELECT * FROM scan WHERE scan_id = %s', (scan_id,))
    scan = cursor.fetchone()
    return render_template('scan_detail.html', scan_id=scan_id, scan=scan)

@views.route('/view_patient_info/<int:patient_id>')
def view_patient_info(patient_id):
    database_session.rollback()
    cursor.execute('SELECT * FROM Patient WHERE ID = %s', (patient_id,))
    patient_info = cursor.fetchone()
    return render_template('view_patient_info.html', patient_info=patient_info)

@views.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient(patient_id):
    database_session.rollback()
    message = None
    message1 = None

    if request.method == 'POST':
        scan_type = request.form.get('scanType')
        test_type = request.form.get('testType')
        appointment_date = request.form.get('appointmentDate')
        additional_notes = request.form.get('additionalNotes')
        hour_minute1 = request.form.get('appointmentHour1')
        message1 = book_scan(scan_type, test_type, appointment_date, additional_notes, patient_id, hour_minute1)

        surgery_type = request.form.get('SurgeryType')
        doctor_name = request.form.get('DoctorName')
        date = request.form.get('appointmentDate2')
        hour_minute = request.form.get('appointmentHour')
        patient_notes = request.form.get('additionalNotes2')
        message = book_surgery(surgery_type, doctor_name, date, hour_minute, patient_notes, patient_id)

    patient = get_patient_by_id(patient_id)
   
    cursor.execute('SELECT * FROM surgery WHERE patient_id = %s', (patient_id,))
    surgerys=cursor.fetchall()
   
    cursor.execute('SELECT * FROM scan WHERE patient_id = %s', (patient_id,))
    scans=cursor.fetchall()
   
    cursor.execute('SELECT * FROM doctor')
    options = cursor.fetchone()

    return render_template('patient.html', patient=patient, surgerys=surgerys, scans=scans, msg=message, msg1=message1, options=options)

@views.route('/get_doctors', methods=['POST'])
def get_doctors():
    database_session.rollback()    
    cursor.execute('SELECT * FROM doctor')
    doctors_data = cursor.fetchall()

    surgery_type = request.form.get('SurgeryType')
    filtered_doctors = [doctor for doctor in doctors_data if doctor[10] == surgery_type]
    return jsonify(filtered_doctors)

@views.route('/admin', methods=['GET', 'POST'])
def admin(msg=None):
    database_session.rollback()
    if request.method == 'POST':
        create_doctor({
            'ssn': request.form['ssn'],
            'email': request.form['email'],
            'password': request.form['password'],
            'user_name': request.form['user_name'],
            'full_name': request.form['full_name'],
            'department': request.form['department'],
            'specialty': request.form['specialty'],
            'gender': request.form['Gender'][0]
        })

    cursor.execute('SELECT * FROM doctor')
    doctors = cursor.fetchall()
    doctors_count = len(doctors)
    cursor.execute('SELECT * FROM patient')
    patients_count = surgeries =len(cursor.fetchall())
    cursor.execute('SELECT * FROM scan')
    scans = cursor.fetchall()
    cursor.execute('SELECT * FROM surgery')
    surgeries = cursor.fetchall()

    app_count = len(scans) + len(surgeries)

    return render_template('admin2.html', doctors=doctors, doctors_count=doctors_count, patient_count=patients_count, app_count=app_count,msg=msg)

@views.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    database_session.rollback()
    cursor.execute('SELECT * FROM doctor WHERE id = %s', (doctor_id,))
    doctor = cursor.fetchone()
    if request.method == 'POST':
        doctor_data = {
            'full_name': request.form.get('full_name'),
            'working_hours': int(request.form.get('working_hours')) if request.form.get('working_hours') else 0,
            'salary': int(request.form.get('salary')) if request.form.get('salary') else 0,
            'phone': request.form.get('phone')[:11] if request.form.get('phone') else '',
            'address': request.form.get('address'),
            'start_work': request.form.get('start'),
            'end_work': request.form.get('end'),
            'department': request.form.get('department'),
            'photo': save_picture(request.files.get('photo'))
        }

        update_doctor_profile(doctor_id, doctor_data)

    return render_template('edit_doctor.html', doctor=doctor)

@views.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor_route(doctor_id):
    database_session.rollback()
    delete_doctor(doctor_id)
    return redirect(url_for('views.admin'))
