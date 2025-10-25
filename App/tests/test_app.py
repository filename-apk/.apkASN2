import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Staff, Employer, Student, InternPosition, ShortlistEntry
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
        hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


class ApplicationUnitTests(unittest.TestCase):

    def setup(self):
          sally = Employer(username="sally", password="sallypass", company_name="TechCorp", position = "IT ")
          bob = Staff(username="bob", password="bobpass", staff_id="S123")
    # --- Test: Create Intern Position ---
    def test_createInternPosition(self):
        """Test creating an internship position."""
        position = self.sally.createInternPosition(
            "Software Intern", "3 months", "1000 USD", 5, "Great internship"
        )
        db.session.add(position)
        db.session.commit()

        openPosition = InternPosition.query.first()
        self.assertIsNotNone(openPosition)
        self.assertEqual(openPosition.title, "Software Intern")
        self.assertEqual(openPosition.duration, "3 months")
        self.assertEqual(openPosition.amount, "1000 USD")
        self.assertEqual(openPosition.description, "Great internship")

    # --- Test: Review Applicants ---
    def test_reviewApplicants(self):
        """Test reviewing applicants for a position."""
        position = self.sally.createInternPosition("Backend Intern", "4 months", "2000 USD", 3, "Work on APIs")
        db.session.add(position)
        db.session.commit()

        shortlist = self.bob.shortlistStudent(position.id)
        db.session.add(shortlist)
        db.session.commit()

        applicants = self.sally.reviewApplicants(position.id)
        self.assertTrue(len(applicants) > 0)
        self.assertEqual(applicants[0].student_id, self.bob.id)

    # --- Test: Make Decision ---
    def test_makeDecision(self):
        """Test making an approval decision on an applicant."""
        position = self.sally.createInternPosition("UI Designer", "3 months", "1500 USD", 2, "Design UIs")
        db.session.add(position)
        db.session.commit()

        shortlist = self.bob.shortlistStudent(position.id)
        db.session.add(shortlist)
        db.session.commit()

        result = self.sally.makeDecision(position.id, self.bob.id, True)
        db.session.commit()

        updated = ShortlistEntry.query.filter_by(position_id=position.id, student_id=self.bob.id).first()
        self.assertTrue(updated.status)
        self.assertEqual(result, "Decision Updated Successfully")

    # --- Test: Shortlist Student ---
    def test_shortlistStudent(self):
        """Test that a student can be shortlisted."""
        position = self.sally.createInternPosition("Data Analyst", "3 months", "2000 USD", 4, "Analyse data")
        db.session.add(position)
        db.session.commit()

        shortlist = self.bob.shortlistStudent(position.id)
        db.session.add(shortlist)
        db.session.commit()

        self.assertIsNotNone(shortlist)
        self.assertEqual(shortlist.student_id, self.bob.id)
        self.assertEqual(shortlist.position_id, position.id)

    # --- Test: View Shortlisted Positions ---
    def test_viewShortlistedPositions(self):
        """Test viewing all positions a student is shortlisted for."""
        pos1 = self.sally.createInternPosition("Backend", "6 months", "2500 USD", 5, "Server dev")
        pos2 = self.sally.createInternPosition("Frontend", "6 months", "2300 USD", 4, "UI dev")
        db.session.add_all([pos1, pos2])
        db.session.commit()

        shortlist1 = self.bob.shortlistStudent(pos1.id)
        shortlist2 = self.bob.shortlistStudent(pos2.id)
        db.session.add_all([shortlist1, shortlist2])
        db.session.commit()

        results = self.bob.viewShortlistedPositions()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].position_id, pos1.id)
        self.assertEqual(results[1].position_id, pos2.id)
















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
        self.assertListEqual([{"id":1, "username":"bob", "type": "user"}, {"id":2, "username":"rick","type":"user"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
      
 
class ApplicationIntegrationTests(unittest.TestCase):
    def test_staff_shortlistStudent(self):
        bob = get_staff(1); 
        rick = get_student(2);
        sally = get_employer(3); 
        position = sally.createInternPosition("Software Intern", "3 months", "6000", 5, "Great internship")
        bob.shortlistStudent(bob, position.positionID, rick.studentID)
        assert rick.studentID in [entry.studentID for entry in position.shortlistEntries]
    
    def test_employer_createInternPosition(self):
        sally = get_employer(3);  
        position = sally.createInternPosition( "Software Intern", "3 months", "6000", 5, "Great internship")

        assert position in sally.internPositions, f"Position{position.title} not found in employer's intern positions"

    def test_employer_reviewApplication(self):
        sally = get_employer(3);  
        rick = get_student(2);
        bob = get_staff(1);
        position = sally.createInternPosition(sally, "Software Intern", "3 months", "1000 USD", 5, "Great internship")
        
        shortlistEntry = bob.shortlistStudent(bob, position.positionID, rick.studentID);
        sally.reviewApplication(sally);
        assert shortlistEntry.studentID == rick.studentID;

    def test_employer_makeDecision(self):
        sally = get_employer(3);  
        rick = get_student(2);
        bob = get_staff(1);
        position = sally.createInternPosition( "Software Intern", "3 months", "1000 USD", 5, "Great internship")
       
        shortlistEntry = bob.shortlistStudent(bob, position.positionID, rick.studentID);
        sally.makeDecision( position.positionID, rick.studentID, "Approved");
        assert shortlistEntry.status == "Approved";


    def test_student_viewShortlistStatus(self):
        rick = get_student(2);
        status = rick.viewShortlistedPositions(rick);
        assert isinstance(status,str);




