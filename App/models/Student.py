from App.database import db
from .User import User

class Student(User):
    __tablename__ = 'student'

    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    gpa = db.Column(db.Float, nullable=False)

    shortlists = db.relationship('Shortlist', back_populates='student', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, name, university, degree, year, gpa):
        super().__init__(username, password)
        self.name = name
        self.university = university
        self.degree = degree
        self.year = year
        self.gpa = gpa