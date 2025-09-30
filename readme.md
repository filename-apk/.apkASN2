![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# 🧱 Flask MVC Internship App Template

A structured Flask application following the **Model-View-Controller (MVC)** architecture. It supports **employers**, **staff**, and **students** with role-specific CLI commands and is ideal for managing internship positions and applications.

🔗 [Demo](https://dcit-flaskmvc.herokuapp.com/) | 📫 [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)

---

## ⚙️ Dependencies

- Python 3.9.10
- Packages listed in `requirements.txt`

The `venv` folder contains a preconfigured virtual environment using Python 3.9.10 with all dependencies installed. If not required on your system, you can delete it and instead use your own interpreter.

To change the Python interpreter in VS Code:

- Press `CTRL + SHIFT + P`
- Select **“Python: Select Interpreter”**
- Choose your Python 3.9.10 installation

Alternatively, edit `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "venv/bin/python",
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true,
  "python-envs.pythonProjects": []
}
```

# User Creation Commands

```bash
flask create-employer <username> <password>
```
- Create an employer user account

```bash
flask create-student <username> <password>
```
- Create a student user account

```bash
flask create-staff <username> <password>
```
- Create a staff user account

# Employer Commands

```bash
$ flask create-position
```
- Enables and a selected employer to open an intern position

```bash
$ flask review-applicants
```
- Enables a selected employer to see the shortlisted individuals and their decision status for all their opened positions

```bash
$ flask make-decision
```
- Enables a selected employer to make a decision to approve a shortlisted student for an intern position or reject them

# Staff Commands

```bash
$ flask shortlist-student
```
- Enables a selected staff memeber to shortlist a chosen student for an open intern position

# Student Commands

```bash
$ flask shortlisted-positions
```
- Enables a selected student to view all the positions they have been shortlisted for as well as the decision made regarding their application (Pending, Approved, Rejected)

# Database Initialization Commands

```bash
$ flask init
```
- Initialize database without data

```bash
$ flask init-default
```
- Initialize database with a default dataset. This creates:

        Employers: Bill Gates, Jeff Bezos, Vince McMahon

        Students: Alice, Bob, Charlie

        Staff: Prof. Johnson, Dr. Lee, Keith

        Intern Positions: 3 predefined internship

As user commands require a simple 'login' to validate the existance of seperately defined users, please take note of the username and password attributes of any default accounts utilized. For newly created accounts, be sure to remember those login details as it is very much needed to use the application

```
Employers:

BillGates
username="billygates", password="iLoveMicrosoft"

JeffBezos
username="thereal_baldy", password="amazon123"

VinceMcMahon
username="moneybagsvince", password="wwe4life"
```

```
Students:

Alice
username="alice_w", password="alicepass"

Bob
username="bob_b", password="bobpass"

Charlie
username="charlie_b", password="charliepass"
```

```
Staff:

ProfJohnson
username="prof_johnson", password="johnsonpass"

DrLee
Staff(username="dr_lee", password="leepass"

Keith
username="keith_r", password="greatistheUNC"
```

```
Intern Positions:

Position1 = InternPosition(employer=BillGates, title="Software Engineering Intern", duration="3 Months", stipend=True, amount=6000.00, description="Work on cutting-edge software solutions.")
Position2 = InternPosition(employer=JeffBezos, title="Data Analyst Intern", duration="6 Months", stipend=True, amount=7000.00, description="Analyze large datasets to drive business decisions.")
Position3 = InternPosition(employer=VinceMcMahon, title="Marketing Intern", duration="3 Months", stipend=False, amount=None, description="Assist in marketing campaigns and social media management.")
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```
