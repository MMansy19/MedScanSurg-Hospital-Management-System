CREATE TABLE Doctor (
    ID SERIAL PRIMARY KEY,
    SSN INT,
    email VARCHAR(100),
    password VARCHAR(50) NOT NULL ,
    user_name VARCHAR(50) UNIQUE NOT NULL ,
    full_name VARCHAR(50),
    working_hours INT,
    salary INT,
    phone VARCHAR(11),
    address VARCHAR(30),
    gender VARCHAR(1),
    photo VARCHAR(100),
    speciality VARCHAR(100)
    CONSTRAINT chk_gender CHECK(gender IN ('M','F'))
);

CREATE TABLE Department(
    ID SERIAL PRIMARY KEY,
    name VARCHAR(9),
    location VARCHAR(50),
    CONSTRAINT chk_department CHECK (name IN ('Radiology', 'Surgery'))
);

CREATE TABLE WorksIn(
    department_id INT REFERENCES Department(ID),
    doctor_id INT REFERENCES Doctor(ID),
    date_hired DATE
);

CREATE TABLE Patient (
    ID SERIAL PRIMARY KEY,
    SSN VARCHAR(14),
    email VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL ,
    full_name VARCHAR(100),
    birthdate DATE
);

CREATE TABLE Scan (
    scan_id SERIAL PRIMARY KEY,
    doctor_id INT REFERENCES Doctor(ID),
    price int,
    machine VARCHAR(100)  NOT NULL,
    category VARCHAR(100)  NOT NULL,
    Scan_date DATE,
    photo VARCHAR(100)
);

CREATE TABLE Surgery (
    surgery_id SERIAL PRIMARY KEY,
    doctor_id INT REFERENCES Doctor(ID),
    patient_id INT REFERENCES Patient(patient_id),
    type VARCHAR(50),
    date DATE,
    room_number INT,
    duration INT
);
