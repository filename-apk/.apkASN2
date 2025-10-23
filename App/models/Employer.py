from App.database import db
from .User import User

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
