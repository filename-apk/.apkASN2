from flask import Blueprint, jsonify, request
from App.controllers.auth import login_required
from App.models import Employer
from App.database import db
from App.controllers.EmployerController import createInternPosition, reviewApplicants, makeDecision

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')

@employer_views.route('/api/employers/<int:employer_id>/intern_positions', methods=['POST'])
@login_required(Employer)
def create_intern_position(employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return jsonify({'error': 'Employer not found'}), 404
    
    try:
        data = request.get_json()
        required_fields = ['title', 'duration', 'stipend', 'amount', 'description']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        position = createInternPosition(
            employer=employer,
            title=data['title'],
            duration=data['duration'],
            stipend=data['stipend'],
            amount=data['amount'],
            description=data['description']
        )

        return jsonify({
            'message': 'Intern position created successfully',
            'position_id': position.positionID
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@employer_views.route('/api/employers/<int:employer_id>/review_applicants', methods=['GET'])
@login_required(Employer)
def review_applicants(employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return jsonify({'error': 'Employer not found'}), 404
    
    try:
        applicants = reviewApplicants(employer)
        return jsonify(applicants), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@employer_views.route('/api/employers/<int:employer_id>/make_decision', methods=['POST'])
@login_required(Employer)
def make_decision(employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return jsonify({'error': 'Employer not found'}), 404
    
    try:
        data = request.get_json()
        required_fields = ['positionID', 'studentID', 'decision']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        result = makeDecision(
            employer=employer,
            positionID=data['positionID'],
            studentID=data['studentID'],
            decision=data['decision']
        )

        if result == "Decision Updated Successfully":
            return jsonify({'message': result}), 200
        else:
            return jsonify({'error': result}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500