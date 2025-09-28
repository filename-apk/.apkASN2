from App.database import db

class Shortlist(db.Model):
    __tablename__ = 'shortlist'

    shortlistID = db.Column(db.Integer, primary_key=True)
    staffID = db.Column(db.Integer, db.ForeignKey('staff.staffID'), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    positionID = db.Column(db.Integer, db.ForeignKey('intern_position.positionID'), nullable=False)
    status =  db.Column(db.String(50), default='Pending', nullable=False) # e.g., Pending, Approved, Rejected

    # Bridge Relationships to Staff and Student
    staff = db.relationship('Staff', back_populates='shortlists')
    student = db.relationship('Student', back_populates='shortlists')
    
    # Relationship to InternPosition
    # Back-populates the 'shortlist' relationship in InternPosition
    # ^^ This ensures cascading delete is applied from InternPosition to Shortlist
    shortlistedFor = db.relationship('InternPosition', back_populates='shortlist', lazy=True)

    def __init__(self, staff, student, position):
        self.staff = staff
        self.student = student
        self.shortlistedFor = position