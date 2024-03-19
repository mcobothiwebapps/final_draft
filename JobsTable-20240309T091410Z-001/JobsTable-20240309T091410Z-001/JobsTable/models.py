from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class ApplicationStatus(Enum):
    SUCCESSFUL = "successful"
    REJECT = "reject"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.String(255), nullable=False)
    hours = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)

    # Define foreign key relationship to Department table
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Define a back reference to access department details from Job object

    department_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Job(id={self.id}, title={self.title}, department_name={self.department_name})"


class Reminder:
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.String(50), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    student_number = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def get_id(self):
        return str(self.id)

    # Method to set password securely
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to verify password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_number = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    id_number = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=False, nullable=False)
    course = db.Column(db.String, nullable=False)
    academic_background = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    skills = db.Column(db.String, nullable=False)
    documents = db.relationship('Document', backref='application', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    status = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Application {self.name}>'


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    file_path = db.Column(db.String(255))


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.Text, nullable=False)
    faculty = db.Column(db.String(100), nullable=False)

    jobs = db.relationship('Job', backref='department', lazy=True)

    def __repr__(self):
        return f"Department(id={self.id}, name={self.name})"
