from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

#------- IMPORTS -------#

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a_very_secret_and_long_key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Course(db.Model):
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_summary_json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "createdAt": self.createdAt.isoformat() + 'Z',
            "updatedAt": self.updatedAt.isoformat() + 'Z'
        }
with app.app_context():
    db.create_all()

    if not Course.query.first():
        print("Seeding database with sample course...")
        sample_course = Course(name="Introduction to Web Development", description="Learn the basics of HTML, CSS, and Flask.")
        db.session.add(sample_course)
        db.session.commit()

#------- APP CONFIG + DATABASE CONFIG + LOGIN MANAGER -------#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'], strict_slashes=False) 
def api_endpoint():
    response = {
        "organization": "Student Cyber Games"
    }
    return jsonify(response)

LECTURER_USERNAME = "lecturer"
LECTURER_PASSWORD = "TdA26!"

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = LECTURER_USERNAME
        
    def get_id(self):
        return str(self.id)
    
@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        return User(id=1)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == LECTURER_USERNAME and password == LECTURER_PASSWORD:
            user = User(id=1) 
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/courses', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return jsonify([course.to_summary_json() for course in courses])

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/courses', methods=['POST'])
@login_required
def create_course():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Missing required field: name"}), 400
    new_course = Course(
        name=data.get("name"),
        description=data.get("description", "")
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_summary_json()), 201

@app.route('/courses/<course_uuid>', methods=['PUT'])
@login_required
def update_course(course_uuid):
    course = Course.query.filter_by(uuid=course_uuid).first()
    if course is None:
        return jsonify({"message": "Course not found"}), 404
    
    data = request.get_json()

    if 'name' in data:
        course.name = data['name']

    if 'description' in data:
        course.description = data['description']

    db.session.commit()

    return jsonify(course.to_summary_json()), 200

@app.route('/courses/<course_uuid>', methods=['DELETE'])
@login_required
def delete_course(course_uuid):
    course = Course.query.filter_by(uuid=course_uuid).first()
    if course is None:
        return jsonify({"message": "Course not found"}), 404
    db.session.delete(course)
    db.session.commit()
    return '', 204

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/courses/<course_uuid>')
def course_detail(course_uuid):
    return render_template('course_detail.html', course_uuid=course_uuid)