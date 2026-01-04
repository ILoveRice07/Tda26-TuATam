import os
from flask import Flask
from flask import Flask, redirect, url_for, request
from extensions import db, login_manager
from models import Course, User

from routes.api import api_bp
from routes.views import views_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a_very_secret_and_long_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'views.login' 

@login_manager.user_loader
def load_user(user_id):
    if user_id == '1':
        return User(id=1)
    return None

@app.route('/courses', methods=['POST'])
def redirect_create_course():
    return redirect(url_for('api.list_courses', **request.args))

@app.route('/courses/<course_uuid>', methods=['PUT', 'DELETE'])
def redirect_update_delete_course(course_uuid):
    return redirect(url_for('api.get_course_detail', course_uuid=course_uuid, **request.args))

app.register_blueprint(api_bp, url_prefix='/api') 
app.register_blueprint(views_bp) 


with app.app_context():
    db.create_all()
    if not Course.query.first():
        print("Seeding database...")
        sample_course = Course(name="Introduction to Web Development", description="Basics of Flask.")
        db.session.add(sample_course)
        db.session.commit()