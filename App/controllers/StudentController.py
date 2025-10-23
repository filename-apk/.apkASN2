from App.models import Student
from App.database import db

def viewShortlistedPositions(student):
        shortlistedPositions = []

        for entry in student.shortlistings:
            position = entry.shortlistedFor
            shortlistedPositions.append(f"ID: {position.positionID} | Title: {position.title} | Employer: {position.createdBy.name} - {position.createdBy.position} | Company: {position.createdBy.company} | Duration: {position.duration} | Stipend: {'Yes' if position.stipend else 'No'} | Amount: {position.amount if position.amount else 'N/A'} | Description: {position.description} | Status: {entry.status}")
        return shortlistedPositions