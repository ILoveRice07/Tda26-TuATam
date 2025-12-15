from flask import Blueprint, jsonify, request
from flask_login import login_required
from extensions import db
from models import Course

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def api_endpoint():
    return jsonify({"organization": "Student Cyber Games"})


@api_bp.route('/courses', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return jsonify([course.to_summary_json() for course in courses])

@api_bp.route('/courses', methods=['POST'])
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

@api_bp.route('/courses/<course_uuid>', methods=['GET'])
def get_course_detail(course_uuid):
    course = Course.query.filter_by(uuid=course_uuid).first()
    if course is None:
        return jsonify({"message": "Course not found"}), 404
    return jsonify(course.to_summary_json()), 200

@api_bp.route('/courses/<course_uuid>', methods=['PUT'])
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

@api_bp.route('/courses/<course_uuid>', methods=['DELETE'])
@login_required
def delete_course(course_uuid):
    course = Course.query.filter_by(uuid=course_uuid).first()
    if course is None:
        return jsonify({"message": "Course not found"}), 404
    db.session.delete(course)
    db.session.commit()
    return '', 204