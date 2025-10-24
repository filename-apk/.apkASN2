from App.models import User, Student, Employer, Staff
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_student(username, password, name, university, degree, year, gpa):
    newstudent = Student(username=username, password=password, name=name, university=university, degree=degree, year=year, gpa=gpa)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def create_employer(username, password, name, company, position):
    newemployer = Employer(username=username, password=password, name=name, company=company, position=position)
    db.session.add(newemployer)
    db.session.commit()
    return newemployer

def create_staff(username, password, name, faculty):
    newstaff = Staff(username=username, password=password, name=name, faculty=faculty)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
