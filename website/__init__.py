from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import psycopg2
import psycopg2.extras
db = SQLAlchemy()
DB_NAME = "database.db"

database_session = psycopg2.connect(
    database='postgres',
    port=5432,
    host='localhost',
    user='postgres',
    password= 'admin'
)
cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/database'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

    
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    
    login_manager = LoginManager(app)
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    
  
    @login_manager.user_loader
    def load_user(user_id):
        cursor.execute(f'SELECT * FROM doctor WHERE id ={user_id}')
        doctor = cursor.fetchall()
        return doctor
    
    return app

