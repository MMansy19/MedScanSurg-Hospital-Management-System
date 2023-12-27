from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database ' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/patient')
def patient():
    return render_template('patient.html')

if __name__ == '__main__':
    app.run(debug=True)
db = SQLAlchemy(app)
#  virtualenv venv
# venv/Scripts/activate.bat
