import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Staff, Employer, Student
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    

)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "type":"user"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


    

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None



def get_staff(staffID):
       return Staff.query.get(staffID)

def get_student(studentID):
     return Student.query.get(studentID)

def get_employer(empID):
     return Employer.query.get(empID)


    
 

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob", "type":"user"}, {"id":2, "username":"rick", "type":"user"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
      
 
class ApplicationIntegrationTests(unittest.TestCase):
    def test_staff_shortlistStudent():
        bob = get_staff(1); 
        rick = get_student(2);
        sally = get_employer(3); 
        position = sally.createInternPosition("Software Intern", "3 months", "1000 USD", 5, "Great internship")
        bob.shortlistStudent(bob, position.positionID, rick.studentID)
        assert rick.studentID in [entry.studentID for entry in position.shortlistEntries]
    
    def test_employer_createInternPosition():
        sally = get_employer(3);  
        position = sally.createInternPosition( "Software Intern", "3 months", "1000 USD", 5, "Great internship")
        assert position in sally.internPositions

    def test_employer_reviewApplication():
        sally = get_employer(3);  
        rick = get_student(2);
        bob = get_staff(1);
        position = sally.createInternPosition(sally, "Software Intern", "3 months", "1000 USD", 5, "Great internship")
        
        shortlistEntry = bob.shortlistStudent(bob, position.positionID, rick.studentID);
        sally.reviewApplication(sally);
        assert shortlistEntry.studentID == rick.studentID;

    def test_employer_makeDecision():
        sally = get_employer(3);  
        rick = get_student(2);
        bob = get_staff(1);
        position = sally.createInternPosition( "Software Intern", "3 months", "1000 USD", 5, "Great internship")
       
        shortlistEntry = bob.shortlistStudent(bob, position.positionID, rick.studentID);
        sally.makeDecision( position.positionID, rick.studentID, "Approved");
        assert shortlistEntry.status == "Approved";


    def test_student_viewShortlistStatus():
        rick = get_student(2);
        status = rick.viewShortlistStatus(rick);
        assert isinstance(status,str);




