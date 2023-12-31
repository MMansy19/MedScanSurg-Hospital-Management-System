from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import the datetime module
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from sqlalchemy.exc import IntegrityError
import os
import secrets
from PIL import Image
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired, Length
from os import path
from flask_wtf.file import FileField, FileAllowed



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
    specialty = db.Column(db.String(30))
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    # Relationship with viewsointments
    viewsointments = db.relationship('Appointment', backref='doctor', lazy=True)   

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
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
        
# Add a new model for Scan
class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
 
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
