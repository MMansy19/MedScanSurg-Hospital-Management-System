from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import the datetime module
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.exc import IntegrityError
from os import path
import psycopg2
import psycopg2.extras

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
database_session = psycopg2.connect(
    database='postgres',
    port=5432,
    host='localhost',
    user='postgres',
    password= 'admin'
)

cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)


#
# class Doctor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ssn = db.Column(db.Integer)
#     email = db.Column(db.String(100))
#     password = db.Column(db.String(50), nullable=False)
#     user_name = db.Column(db.String(50), unique=True, nullable=False)
#     full_name = db.Column(db.String(50))
#     working_hours = db.Column(db.Integer)
#     salary = db.Column(db.Integer)
#     phone = db.Column(db.String(11))
#     address = db.Column(db.String(30))
#     # Relationship with appointments
#     appointments = db.relationship('Appointment', backref='doctor', lazy=True)
#
#
# class Patient(db.Model):
#     patient_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100))
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     birthdate = db.Column(db.Date)
#
# class Appointment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
#     doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
#     appointment_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
# db.init_app(app)
# with app.app_context():
#     db.create_all()
#     print('Created Database!')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
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
            # new_patient = Patient(username=username1, name=name1, email=email, password=password1, birthdate=birthdate)
            #
            # db.session.add(new_patient)
            cursor.execute('INSERT INTO patient (username, fullname, email, password, birthdate) VALUES (%s, %s, %s, %s, %s)', (username1, name1, email, password1, birthdate))
            database_session.commit()
            return render_template('login.html')

        elif check_sign:
            user_type = request.form.get('userType')
            username2 = request.form.get('username2')
            password2 = request.form.get('password2')
        
            if(user_type)=='patient':
                # patient = Patient.query.filter_by(username=username2).first()
                cursor.execute('SELECT password FROM patient WHERE username = %s', (username2,))
                password = cursor.fetchone()
                if password is not None:
                    if password[0] == password2:
                        return render_template('index.html')
            
            elif(user_type)=='doctor':
                doctor = cursor.execute('SELECT * FROM doctor WHERE username = %s', (username2,)).fetchone()
                if doctor:
                    if doctor.password ==  password2:
                        return render_template('doctor.html')
                    
            elif(user_type)=='admin':
                #this is admin password and admin username
                if  password2==  'admin_password' and username2 == 'admin_username': 
                    return render_template('admin.html')
    # Render the login form for GET requests
    return render_template('login.html')

@app.route('/doctor')
def doctor():
    
    return render_template('doctor.html')

@app.route('/patient')
def patient():
    return render_template('patient.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        # Get form data
        ssn = request.form['ssn']
        email = request.form['email']
        password = request.form['password']
        user_name = request.form['userName']
        full_name = request.form['fullName']

      # Check if the user_name already exists
      #   existing_doctor = Doctor.query.filter_by(user_name=user_name).first()
        cursor.execute('SELECT * FROM doctor WHERE user_name = %s', (user_name,))
        existing_doctor=cursor.fetchone()
        if not existing_doctor:
            
            # Create a new doctor
            # new_doctor = Doctor(ssn=ssn, email=email, password=password, user_name=user_name,
            #                     full_name=full_name, working_hours=40, salary=80000, phone='1234567890', address='Some Address')
            working_hours = 40
            salary = 80000
            phone = '1234567890'
            address = 'Some Address'
            cursor.execute('INSERT INTO doctor(ssn,email, password, user_name,full_name,working_hours,salary,phone,address) VALUES (%s, %s ,%s,%s,%s,%s,%s,%s,%s)', (ssn,email,password, user_name, full_name,working_hours,salary,phone,address))
            # Add the doctor to the database
            # db.session.add(new_doctor)
            db.session.commit()

    # doctors = Doctor.query.all()
    cursor.execute('SELECT * FROM doctor')
    doctors=cursor.fetchall()
    return render_template('admin.html', doctors=doctors)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
#     if request.method == 'POST':
#         # Handle appointment creation
#         doctor_id = request.form.get('doctor_id')
#         patient_id = current_user.patient_id  # Assuming you're using Flask-Login
#
#         # Check if the appointment time is available (you can add validation logic here)
#
#         new_appointment = Appointment(doctor_id=doctor_id, patient_id=patient_id)
#         db.session.add(new_appointment)
#         db.session.commit()
#         return redirect(url_for('appointments'))
#
#     # Fetch all doctors and pass them to the template
#     doctors = Doctor.query.all()
    return render_template('appointments.html')


@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    # Find the doctor in the database
    # doctor = Doctor.query.get(doctor_id)
    cursor.execute('SELECT * FROM doctor WHERE id = %s', (doctor_id,))
    doctor=cursor.fetchone()
    if request.method == 'POST':
        # Update the doctor's information
        # doctor.email = request.form['email']
        # doctor.password = request.form['password']
        # doctor.full_name = request.form['fullName']
        # doctor.working_hours = request.form['working_hours']
        # doctor.salary = request.form['salary']
        # doctor.phone = request.form['phone']
        # doctor.address = request.form['address']
        cursor.execute('UPDATE doctor SET email = %s WHERE id = %s', (request.form['email'], doctor_id))
        cursor.execute('UPDATE doctor SET password = %s WHERE id = %s', (request.form['password'], doctor_id))
        cursor.execute('UPDATE doctor SET full_name = %s WHERE id = %s', (request.form['fullName'], doctor_id))
        cursor.execute('UPDATE doctor SET working_hours = %s WHERE id = %s', (request.form['working_hours'], doctor_id))
        cursor.execute('UPDATE doctor SET salary = %s WHERE id = %s', (request.form['salary'], doctor_id))
        cursor.execute('UPDATE doctor SET phone = %s WHERE id = %s', (request.form['phone'], doctor_id))
        cursor.execute('UPDATE doctor SET address = %s WHERE id = %s', (request.form['address'], doctor_id))
        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for('admin'))

    # Render the edit doctor form with the current information
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
        # Find the doctor in the database
        cursor.execute('SELECT * FROM doctor WHERE id = %s', (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            cursor.execute('DELETE FROM doctor WHERE id = %s', (doctor_id,))
            db.session.commit()
        # Remove the doctor from the database
        # db.session.delete(doctor)
        return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)
    
#  virtualenv venv
# cd C:\db_project\website
# venv\Scripts\activate
# python app.py