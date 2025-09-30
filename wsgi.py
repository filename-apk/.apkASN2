import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )

from App.models import Employer, Staff, Student, InternPosition, ShortlistEntry

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# Database Initialization Commands

@app.cli.command("init", help="Creates and initializes the the database without data")
def init():
    initialize()
    print('Blank Database Initialized')

@app.cli.command("init-default", help="Creates and initializes the database with a default dataset")
def initDefault():
    initialize()

    BillGates = Employer(username="billygates", password="iLoveMicrosoft", name="Bill Gates", company="Microsoft", position="Founder")
    JeffBezos = Employer(username="thereal_baldy", password="amazon123", name="Jeff Bezos", company="Amazon", position="Founder & CEO")
    VinceMcMahon = Employer(username="moneybagsvince", password="wwe4life", name="Vince McMahon", company="WWE", position="Chairman & CEO")
    
    print('Initializing Default Employers Records...')
    db.session.add_all([BillGates, JeffBezos, VinceMcMahon])

    Alice = Student(username="alice_w", password="alicepass", name="Alice Wonderland", university="Harvard University", degree="Computer Science", year=2, gpa=3.8)
    Bob = Student(username="bob_b", password="bobpass", name="Bobby Brown", university="Stanford University", degree="Business Administration", year=3, gpa=3.5)
    Charlie = Student(username="charlie_b", password="charliepass", name="Charlie Brown", university="MIT", degree="Mechanical Engineering", year=4, gpa=3.9)
    
    print('Initializing Default Students Records...')
    db.session.add_all([Alice, Bob, Charlie])
    
    ProfJohnson = Staff(username="prof_johnson", password="johnsonpass", name="Prof. Emily Johnson", faculty="Business")
    DrLee = Staff(username="dr_lee", password="leepass", name="Dr. Michael Lee", faculty="Computer Science")
    Keith = Staff(username="keith_r", password="greatistheUNC", name="Keith BaldHead RowRow", faculty="Poli-Tricks Science")
    
    print('Initializing Default Staff Records...')
    db.session.add_all([ProfJohnson, DrLee, Keith])

    Position1 = InternPosition(employer=BillGates, title="Software Engineering Intern", duration="3 Months", stipend=True, amount=6000.00, description="Work on cutting-edge software solutions.")
    Position2 = InternPosition(employer=JeffBezos, title="Data Analyst Intern", duration="6 Months", stipend=True, amount=7000.00, description="Analyze large datasets to drive business decisions.")
    Position3 = InternPosition(employer=VinceMcMahon, title="Marketing Intern", duration="3 Months", stipend=False, amount=None, description="Assist in marketing campaigns and social media management.")

    print('Initializing Default Intern Positions Records...')
    db.session.add_all([Position1, Position2, Position3])

    db.session.commit()
    print('Database Intialized and Populated')

# User Creation Commands

@app.cli.command("create-employer", help="Creates an employer")
@click.argument("username")
@click.argument("password")
def createEmployer(username, password):
    name = click.prompt("Enter The Employer's Name")
    company = click.prompt("Enter Their Company's Name")
    position = click.prompt("Enter Their Position")
    newEmployer = Employer(username=username, password=password, name=name, company=company, position=position)
    db.session.add(newEmployer)
    db.session.commit()
    print(f'Employer {username} created!')

@app.cli.command("create-staff", help="Creates a staff member")
@click.argument("username")
@click.argument("password")
def createStaff(username, password):
    name = click.prompt("Enter The Staff's Name")
    faculty = click.prompt("Enter Their Faculty")
    newStaff = Staff(username=username, password=password, name=name, faculty=faculty)
    db.session.add(newStaff)
    db.session.commit()
    print(f'Staff {username} created!')

@app.cli.command("create-student", help="Creates a student")
@click.argument("username")
@click.argument("password")
def createStudent(username, password):
    name = click.prompt("Enter The Student's Name")
    university = click.prompt("Enter Their University")
    degree = click.prompt("Enter Their Degree")
    year = click.prompt("Enter Their Year of Study (i.e. First Year = 1, Second Year = 2, etc...)", type=int)
    gpa = click.prompt("Enter Their GPA", type=float)
    newStudent = Student(username=username, password=password, name=name, university=university, degree=degree, year=year, gpa=gpa)
    db.session.add(newStudent)
    db.session.commit()
    print(f'Student {username} created!')

# Employer Action Commands

@app.cli.command("create-position", help="Creates an internship position (Employer Only)")
def createInternPosition():
    employers = Employer.query.all()
    if not employers:
        print("No Employers Found. Please Register An Employer Account First")
        return

    print("Registered Employers:")
    for employer in employers:
        print(f"    Name - {employer.name} | Company - {employer.company} | Position - {employer.position} | Username - {employer.username}")


    username = click.prompt("Enter The Username of The Employer Opening This Intern Position")
    selectedEmployer = Employer.query.filter_by(username=username).first()
    if not selectedEmployer:
        print("Employer Not Found")
        return
    
    for i in range(3):
        password = click.prompt("Enter The Employer's Password", hide_input=True)
        if not selectedEmployer.check_password(password):
            if i == 2:
                print("Too Many Failed Attempts. Access Denied")
                return
            print("Incorrect Password. Try Again")
        else:
            break
    
    title = click.prompt("Enter The Title of The Intern Position")
    duration = click.prompt("Enter The Duration of The Internship (E.g., 3 months, 6 months, etc...)")

    stipend_input = click.prompt("Is There a Stipend? (Yes/No)", type=click.Choice(['Yes', 'No'], case_sensitive=False))
    if stipend_input.lower() == 'no':
        stipend = False
        amount = None
    else:
        stipend = True
        amount = click.prompt("Enter The Amount of The Stipend (E.g., 5000.00)", type=float)
    
    description = click.prompt("Enter A Brief Description of The Intern Position")

    newPosition = selectedEmployer.createInternPosition(title=title, duration=duration, stipend=stipend, amount=amount, description=description)
    print(f'Intern Position - {newPosition.title} (ID: {newPosition.positionID}) Created Successfully!')

@app.cli.command("review-applicants", help="Review shortlisted students for open positions (Employer Only)")
def reviewApplicants():
    employers = Employer.query.all()
    if not employers:
        print("No Employers Found. Please Register An Employer Account First And Open An Intern Position")
        return
    
    print("Registered Employers:")
    for employer in employers:
        print(f"    Name - {employer.name} | Company - {employer.company} | Position - {employer.position} | Username - {employer.username}")
    
    username = click.prompt("Enter The Username of The Employer Reviewing Applicants")
    selectedEmployer = Employer.query.filter_by(username=username).first()
    if not selectedEmployer:
        print("Employer Not Found")
        return
    
    for i in range(3):
        password = click.prompt("Enter The Employer's Password", hide_input=True)
        if not selectedEmployer.check_password(password):
            if i == 2:
                print("Too Many Failed Attempts. Access Denied")
                return
            print("Incorrect Password. Try Again")
        else:
            break
    
    applicants_by_position = selectedEmployer.reviewApplicants()
    if not applicants_by_position:
        print("Either No Applicants Found For Any Open Positions Or No Open Positions Found")
        return
    
    for position, applicants in applicants_by_position.items():
        print(f"\nPosition: {position}")
        if not applicants:
            print("    No Applicants Shortlisted Yet")
        else:
            for applicant in applicants:
                print(f"    {applicant}")

@app.cli.command("make-decision", help="Make a decision on a shortlisted student (Employer Only)")
def makeDecision():
    employers = Employer.query.all()
    if not employers:
        print("No Employers Found. Please Register An Employer Account First, Open An Intern Position and Have Staff Shortlist Students For The Position")
        return
    
    print("Registered Employers:")
    for employer in employers:
        print(f"    Name - {employer.name} | Company - {employer.company} | Position - {employer.position} | Username - {employer.username}")
    
    username = click.prompt("Enter The Username of The Employer Making A Decision")
    selectedEmployer = Employer.query.filter_by(username=username).first()
    if not selectedEmployer:
        print("Employer Not Found")
        return
    
    for i in range(3):
        password = click.prompt("Enter The Employer's Password", hide_input=True)
        if not selectedEmployer.check_password(password):
            if i == 2:
                print("Too Many Failed Attempts. Access Denied")
                return
            print("Incorrect Password. Try Again")
        else:
            break
    
    positions = selectedEmployer.openPositions
    if not positions:
        print("No Open Positions Found. Please Open An Intern Position First And Have Staff Shortlist Students For The Position")
        return
    
    applicants_by_position = selectedEmployer.reviewApplicants()
    if not applicants_by_position:
        print("No Applicants Found For Any Open Positions")
        return
    
    for position, applicants in applicants_by_position.items():
        print(f"\nPosition: {position}")
        if not applicants:
            print("    No Applicants Shortlisted Yet")
        else:
            for applicant in applicants:
                print(f"    {applicant}")
    
    positionID = click.prompt("Enter The ID of The Intern Position To Make A Decision On", type=int)
    studentID = click.prompt("Enter The ID of The Student To Make A Decision On", type=int)
    decision = click.prompt("Enter Your Decision (Approved/Rejected)", type=click.Choice(['Approved', 'Rejected'], case_sensitive=False))
    result = selectedEmployer.makeDecision(positionID=positionID, studentID=studentID, decision=decision)
    print(result)

# Staff Action Commands

@app.cli.command("shortlist-student", help="Shortlist a student for an intern position (Staff Only)")
def shortlistStudent():
    staffMembers = Staff.query.all()
    if not staffMembers:
        print("No Staff Members Found. Please Register A Staff Account First")
        return
    
    print("Registered Staff Members:")
    for staff in staffMembers:
        print(f"    Name - {staff.name} | Faculty - {staff.faculty} | Username - {staff.username}")
    
    username = click.prompt("Enter The Username of The Staff Shortlisting a Student")
    selectedStaff = Staff.query.filter_by(username=username).first()
    if not selectedStaff:
        print("Staff Member Not Found")
        return
    
    for i in range(3):
        password = click.prompt("Enter The Staff's Password", hide_input=True)
        if not selectedStaff.check_password(password):
            if i == 2:
                print("Too Many Failed Attempts. Access Denied")
                return
            print("Incorrect Password. Try Again")
        else:
            break
    
    students = Student.query.all()
    if not students:
        print("No Students Found. Please Register A Student Account First")
        return
    
    print("Registered Students:")
    for student in students:
        print(f"    ID - {student.studentID} | Name - {student.name} | University - {student.university} | Degree - {student.degree} | Year - {student.year} | GPA - {student.gpa}")
    
    studentID = click.prompt("Enter The ID of The Student to Shortlist", type=int)
    selectedStudent = Student.query.get(studentID)
    if not selectedStudent:
        print("Student Not Found")
        return
    
    positions = InternPosition.query.all()
    if not positions:
        print("No Intern Positions Found. Please Have An Employer Open An Intern Position First")
        return
    
    print("Available Intern Positions:")
    for position in positions:
        print(f"    ID - {position.positionID} | Title - {position.title} | Employer - {position.createdBy.name} - {position.createdBy.position} | Company - {position.createdBy.company} | Duration - {position.duration} | Stipend - {'Yes' if position.stipend else 'No'} | Amount - {position.amount if position.amount else 'N/A'} | Description - {position.description}")
    
    positionID = click.prompt("Enter The ID of The Intern Position to Shortlist The Student For", type=int)
    selectedPosition = InternPosition.query.get(positionID)
    if not selectedPosition:
        print("Intern Position Not Found")
        return
    
    # Check if the student is already shortlisted for this position
    existingEntry = ShortlistEntry.query.filter_by(staffID=selectedStaff.staffID, studentID=selectedStudent.studentID, positionID=selectedPosition.positionID).first()
    if existingEntry:
        print(f"Student {selectedStudent.name} is already shortlisted for the position {selectedPosition.title}.")
        return
    
    selectedStaff.shortlistStudent(student=selectedStudent, position=selectedPosition)
    print(f'Student {selectedStudent.name} Has Been Shortlisted For The Position {selectedPosition.title} by Staff {selectedStaff.name}.')

# Studdent Action Commands

@app.cli.command("shortlisted-positions", help="View the positions a student has been shortlisted for")
def viewShortlistedPositions():
    students = Student.query.all()
    if not students:
        print("No Students Found. Please Register A Student Account First And Have Staff Shortlist Them")
        return
    
    print("Registered Students:")
    for student in students:
        print(f"    Name - {student.name} | University - {student.university} | Degree - {student.degree} | Year - {student.year} | GPA - {student.gpa} | Username - {student.username}")
    
    username = click.prompt("Enter The Username of The Student Viewing Their Shortlisted Positions")
    selectedStudent = Student.query.filter_by(username=username).first()
    if not selectedStudent:
        print("Student Not Found")
        return
    
    for i in range(3):
        password = click.prompt("Enter The Student's Password", hide_input=True)
        if not selectedStudent.check_password(password):
            if i == 2:
                print("Too Many Failed Attempts. Access Denied")
                return
            print("Incorrect Password. Try Again")
        else:
            break
    
    shortlistedPositions = selectedStudent.viewShortlistedPositions()
    if not shortlistedPositions:
        print("No Shortlisted Positions Found")
        return
    
    print(f"\nShortlisted Positions for {selectedStudent.name}:")
    for position in shortlistedPositions:
        print(f"    {position}")   


'''
General User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>

user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)