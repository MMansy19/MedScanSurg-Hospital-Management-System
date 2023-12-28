from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import the datetime module
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.exc import IntegrityError
from os import path

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer)
    email = db.Column(db.String(100))
    password = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(50))
    working_hours = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    phone = db.Column(db.String(11))
    address = db.Column(db.String(30))
    
class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)

db.init_app(app)  
with app.app_context():
    db.create_all()
    print('Created Database!')


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
            new_patient = Patient(username=username1, name=name1, email=email, password=password1, birthdate=birthdate)

            db.session.add(new_patient)
            db.session.commit()
            # db.session.rollback()
            flash('Email address already exists. Please use a different email.', 'error')
                # Redirect or render the registration form again
            return render_template('login.html')

        elif check_sign:
            user_type = request.form.get('userType')
            username2 = request.form.get('username2')
            password2 = request.form.get('password2')
        
            if(user_type)=='patient':
                patient = Patient.query.filter_by(username=username2).first()
                if patient:
                    if patient.password ==  password2:
                        flash('Logged in successfully!', category='success')
                        # login_user(patient, remember=True)
                        return render_template('index.html')
                    else:
                        flash('Incorrect password, try again.', category='error')
                else:
                    flash('Username does not exist.', category='error')
            
            elif(user_type)=='doctor':
                doctor = Doctor.query.filter_by(user_name=username2).first()
                if doctor:
                    if doctor.password ==  password2:
                        flash('Logged in successfully!', category='success')
                        # login_user(doctor, remember=True)
                        return render_template('doctor.html')
                    else:
                        flash('Incorrect password, try again.', category='error')
                else:
                    flash('Username does not exist.', category='error')
                
                return render_template('index.html')
        
            elif(user_type)=='admin':
                #this is admin password and admin username
                if  password2==  'admin_password' and username2 == 'admin_username': 
                    return render_template('admin.html')
                else:
                    flash('Incorrect password, try again.', category='error')

                
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

        # Create a new doctor
        new_doctor = Doctor(ssn=ssn, email=email, password=password, user_name=user_name,
                            full_name=full_name, working_hours=40, salary=80000, phone='1234567890', address='Some Address')

        # Add the doctor to the database
        db.session.add(new_doctor)
        db.session.commit()

    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
    
#  virtualenv venv
# cd C:\db_project\website
# venv/Scripts/activate
# python app.py
