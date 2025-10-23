from App.models import Staff
from App.models import ShortlistEntry
from App.database import db

def shortlistStudent(staff, student, position):
    newEntry = ShortlistEntry(staff, student, position)
    db.session.add(newEntry)
    db.session.commit()
    return newEntry