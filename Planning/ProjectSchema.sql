CREATE TABLE Doctor (
    ID SERIAL PRIMARY KEY,
    SSN VARCHAR(30),
    email VARCHAR(100),
    user_name VARCHAR(50) UNIQUE NOT NULL ,
    password VARCHAR(50) NOT NULL ,
    full_name VARCHAR(50),
    working_hours INT,
    salary INT,
    phone VARCHAR(11),
    address VARCHAR(30),
    specialty VARCHAR(100),
    gender VARCHAR(1),
    photo VARCHAR(100),
    department VARCHAR(100),
    start_work INT,
    end_work INT
    CONSTRAINT chk_gender CHECK(gender IN ('M','F'))
    CONSTRAINT chk_department CHECK (department IN ('Radiology', 'Surgery'))

);

CREATE TABLE Patient (
    ID SERIAL PRIMARY KEY,
    SSN VARCHAR(30),
    email VARCHAR(100) NOT NULL,
    user_name VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL ,
    full_name VARCHAR(100),
    birthdate DATE
);

    CREATE TABLE Scan
    (
        scan_id SERIAL PRIMARY KEY,
        doctor_id INTEGER REFERENCES doctor(ID),
        price         integer,
        machine       varchar(100) not null,
        category      varchar(100) not null,
        report        varchar(100),
        date          date,
        patient_notes varchar(100),
        patient_id    integer constraint patient_id___fk references patient,
        time          varchar(10)
    );

    CREATE TABLE Surgery (
        surgery_id SERIAL PRIMARY KEY,
        doctor_id INT REFERENCES Doctor(ID),
        patient_id INT REFERENCES Patient(ID),
        type VARCHAR(50),
        date DATE,
        room_number INT,
        duration INT
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



CREATE TABLE Do (
    scan_id INT REFERENCES Scan(scan_id),
    patient_id INT REFERENCES Patient(patient_id),
    Scan_date DATE
);


CREATE TABLE Admin(
    ID SERIAL PRIMARY KEY,
    SSN INT,
    email VARCHAR(100),
    password VARCHAR(50) NOT NULL ,
    user_name VARCHAR(50) UNIQUE NOT NULL ,
    full_name VARCHAR(50)
);