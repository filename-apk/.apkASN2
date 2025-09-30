from App.database import db
from .User import User
from .ShortlistEntry import ShortlistEntry

class Staff(User):
    __tablename__ = 'staff'

    staffID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)

    shortlists = db.relationship('ShortlistEntry', back_populates='staff', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, username, password, name, faculty):
        super().__init__(username, password)
        self.name = name
        self.faculty = faculty
    
    def shortlistStudent(self, student, position):
        newEntry = ShortlistEntry(staff=self, student=student, position=position)
        db.session.add(newEntry)
        db.session.commit()
        return newEntry
