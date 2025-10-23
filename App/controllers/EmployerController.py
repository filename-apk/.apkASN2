from App.models import Employer
from App.models import InternPosition, ShortlistEntry
from App.database import db

def createInternPosition(employer, title, duration, stipend, amount, description):
        newPosition = InternPosition(employer=employer, title=title, duration=duration, stipend=stipend, amount=amount, description=description)
        db.session.add(newPosition)
        db.session.commit()
        return newPosition

def reviewApplicants(employer):
        applicants_by_position = {}

        for position in employer.openPositions:
            # Composite Key: "Title (ID: 12)"
            key = f"{position.title} (ID: {position.positionID})"
            applicants_by_position[key] = []

            for entry in position.shortlist:
                student = entry.student
                # Composite Value: "Student Name (ID: 7)"
                applicants_by_position[key].append(f"(Status: {entry.status}) | ID: {student.studentID} | {student.name} | University: {student.university} | Degree: {student.degree} | Year Of Study: {student.year} | GPA: {student.gpa}")

        return applicants_by_position

def makeDecision(employer, positionID, studentID, decision):
        position = InternPosition.query.get(positionID)
        if not position:
            return "Position Not Found"
        
        if position.empID != employer.empID:
            return "Unauthorized Action: This Position Was Not Opened By You"

        shortlistEntry = ShortlistEntry.query.filter_by(positionID=positionID, studentID=studentID).first()
        if not shortlistEntry:
            return "Shortlist Entry Not Found"
        
        if decision not in ['Approved', 'Rejected']:
            return "Invalid Decision. Must be 'Approved' or 'Rejected'"
        
        shortlistEntry.status = decision
        db.session.commit()
        return "Decision Updated Successfully"