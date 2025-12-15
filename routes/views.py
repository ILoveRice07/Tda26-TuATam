from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User

views_bp = Blueprint('views', __name__)

LECTURER_USERNAME = "lecturer"
LECTURER_PASSWORD = "TdA26!"

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard')) 
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == LECTURER_USERNAME and password == LECTURER_PASSWORD:
            user = User(id=1) 
            login_user(user)
            return redirect(url_for('views.dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@views_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))

@views_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@views_bp.route('/courses', methods=['GET'])
def courses():
    return render_template('courses.html')

@views_bp.route('/courses/<course_uuid>')
def course_detail(course_uuid):
    return render_template('course_detail.html', course_uuid=course_uuid)