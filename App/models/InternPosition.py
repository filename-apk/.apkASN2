from App.database import db

class InternPosition(db.Model):
    __tablename__ = 'intern_position'

    positionID = db.Column(db.Integer, primary_key=True)
    empID = db.Column(db.Integer, db.ForeignKey('employer.empID'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    stipend = db.Column(db.Boolean, nullable=False)
    amount = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=False)

    # Relationship to Employer
    # Back-populates the 'openPositions' relationship in Employer
    # ^^ This ensures cascading delete is applied from Employer to InternPosition
    createdBy = db.relationship('Employer', back_populates='openPositions', lazy=True)

    # Relationship to Shortlist
    shortlist = db.relationship('Shortlist', back_populates='shortlistedFor', lazy=True, cascade="all, delete-orphan")

    def __init__(self, employer, empID, title, duration, stipend, amount, description):
        self.createdBy = employer  # Sets the relationship and FK automatically
        self.title = title
        self.duration = duration
        self.stipend = stipend
        self.amount = amount
        self.description = description