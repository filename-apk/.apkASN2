from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views
from werkzeug.security import generate_password_hash

from App.database import db

from App.controllers import (
    create_user,
    create_student,
    create_employer,
    create_staff,
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/api/student', methods=['POST'])
def register_student():
    try:
        data = request.get_json()

        required_fields = ['username', 'password', 'name', 'university', 'degree', 'year', 'gpa']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        hashed_password = generate_password_hash(str(data['password']))

        student = create_student(
            username=data['username'],
            password=hashed_password,
            name=data['name'],
            university=data['university'],
            degree=data['degree'],
            year=data['year'],
            gpa=data['gpa']
        )

        return jsonify({
            'message': 'Student registered successfully',
            'student_id': student.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_views.route('/api/employer', methods=['POST'])
def register_employer():
    try:
        data = request.get_json()

        required_fields = ['username', 'password', 'name', 'position', 'company']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        hashed_password = generate_password_hash(str(data['password']))

        employer = create_employer(
            username=data['username'],
            password=hashed_password,
            name=data['name'],
            position=data['position'],
            company=data['company']
        )

        return jsonify({
            'message': 'Employer registered successfully',
            'employer_id': employer.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_views.route('/api/staff', methods=['POST'])
def register_staff():
    try:
        data = request.get_json()

        required_fields = ['username', 'password', 'name', 'faculty']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        hashed_password = generate_password_hash(str(data['password']))

        staff = create_staff(
            username=data['username'],
            password=hashed_password,
            name=data['name'],
            faculty=data['faculty']
        )

        return jsonify({
            'message': 'Staff registered successfully',
            'staff_id': staff.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')