from flask import Blueprint, jsonify, request
from App.controllers.auth import login_required
from App.models import Staff, Student, InternPosition
from App.database import db
from App.controllers.StaffController import shortlistStudent

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/api/staff/<int:staff_id>/shortlist', methods=['POST'])
@login_required(Staff)
def shortlist_student(staff_id):
    try:
        data = request.get_json()

        required_fields = ['student_id', 'position_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({'error': 'Staff member not found'}), 404

        student = Student.query.get(data['student_id'])
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        position = InternPosition.query.get(data['position_id'])
        if not position:
            return jsonify({'error': 'Intern position not found'}), 404

        new_entry = shortlistStudent(staff, student, position)

        return jsonify({
            'message': 'Student shortlisted successfully',
            'shortlist_entry_id': new_entry.shortlistID
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500