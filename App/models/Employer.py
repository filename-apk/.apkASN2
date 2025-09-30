from App.database import db
from .User import User
from .InternPosition import InternPosition
from .ShortlistEntry import ShortlistEntry

class Employer(User):
    __tablename__ = 'employer'

    empID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False)

    # Relationship to InternPosition
    openPositions = db.relationship('InternPosition', back_populates='createdBy', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'employer',
    }

    def __init__(self, username, password, name, company, position):
        super().__init__(username, password)
        self.name = name
        self.company = company
        self.position = position

    # More Functionality To Add
    def createInternPosition(self, title, duration, stipend, amount, description):
        newPosition = InternPosition(employer=self, title=title, duration=duration, stipend=stipend, amount=amount, description=description)
        db.session.add(newPosition)
        db.session.commit()
        return newPosition
    
    def reviewApplicants(self):
        applicants_by_position = {}

        for position in self.openPositions:
            # Composite Key: "Title (ID: 12)"
            key = f"{position.title} (ID: {position.positionID})"
            applicants_by_position[key] = []

            for entry in position.shortlist:
                student = entry.student
                # Composite Value: "Student Name (ID: 7)"
                applicants_by_position[key].append(f"(Status: {entry.status}) | ID: {student.studentID} | {student.name} | University: {student.university} | Degree: {student.degree} | Year Of Study: {student.year} | GPA: {student.gpa}")

        return applicants_by_position
    

    def makeDecision(self, positionID, studentID, decision):
        position = InternPosition.query.get(positionID)
        if not position:
            return "Position Not Found"
        
        if position.empID != self.empID:
            return "Unauthorized Action: This Position Was Not Opened By You"

        shortlistEntry = ShortlistEntry.query.filter_by(positionID=positionID, studentID=studentID).first()
        if not shortlistEntry:
            return "Shortlist Entry Not Found"
        
        if decision not in ['Approved', 'Rejected']:
            return "Invalid Decision. Must be 'Approved' or 'Rejected'"
        
        shortlistEntry.status = decision
        db.session.commit()
        return "Decision Updated Successfully"
