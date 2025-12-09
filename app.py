from flask import Flask, jsonify, render_template, request
import uuid
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'], strict_slashes=False) 
def api_endpoint():
    response = {
        "organization": "Student Cyber Games"
    }
    return jsonify(response)

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/courses', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return jsonify([course.to_summary_json() for course in courses])

@app.route('/api/courses', methods=['POST'])
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