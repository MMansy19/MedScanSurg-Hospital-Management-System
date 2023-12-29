from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

# Define your models (tables)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn = db.Column(db.Integer)
    email = db.Column(db.String(100))
    password = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(50))

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
    # gender = db.Column(db.String(1), CheckConstraint("gender IN ('M','F')"))
    
class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)
        

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(9))
    location = db.Column(db.String(50))
    # Define relationships if needed

class WorksIn(db.Model):
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), primary_key=True)
    date_hired = db.Column(db.Date)
    # Define relationships if needed
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# Add similar models for other tables