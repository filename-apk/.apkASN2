from flask import Blueprint, jsonify
from App.controllers.auth import login_required
from App.models import Student
from App.database import db
from App.controllers.StudentController import viewShortlistedPositions

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/api/students/<int:student_id>/shortlistings', methods=['GET'])
@login_required(Student)
def get_student_shortlisted_positions(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    shortlisted_positions = viewShortlistedPositions(student)

    response_data = []
    for entry in student.shortlistings:
        position = entry.shortlistedFor
        response_data.append({
            'positionID': position.positionID,
            'title': position.title,
            'employer': {
                'name': position.createdBy.name,
                'position': position.createdBy.position,
                'company': position.createdBy.company
            },
            'duration': position.duration,
            'stipend': position.stipend,
            'amount': position.amount if position.amount else None,
            'description': position.description,
            'status': entry.status
    })

    return jsonify({
        'studentID': student.id,
        'shortlistedCount': len(response_data),
        'shortlistedPositions': response_data
    }), 200
