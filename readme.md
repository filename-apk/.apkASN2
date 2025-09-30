![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# 🧱 Flask MVC Internship App Template

A structured Flask application following the **Model-View-Controller (MVC)** architecture. It supports **employers**, **staff**, and **students** with role-specific CLI commands

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

## 👥 User Creation Commands

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

## 🧑‍💼 Employer Commands

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

## 🧑‍🏫 Staff Commands

```bash
$ flask shortlist-student
```
- Enables a selected staff memeber to shortlist a chosen student for an open intern position

## 🎓 Student Commands

```bash
$ flask shortlisted-positions
```
- Enables a selected student to view all the positions they have been shortlisted for as well as the decision made regarding their application (Pending, Approved, Rejected)

## 🛠️ Database Initialization Commands

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

Name            Username            Password
BillGates       billygates          iLoveMicrosoft

JeffBezos       thereal_baldy       amazon123

VinceMcMahon    moneybagsvince       wwe4life
```

```
Students:

Name        Username         Password
Alice       alice_w          alicepass

Bob         bob_b            bobpass

Charlie     charlie_b        charliepass
```

```
Staff:

Name            Username           Password
ProfJohnson     prof_johnson       johnsonpass

DrLee           dr_lee             leepass

Keith           keith_r             greatistheUNC
```

```
Intern Positions:
1. Software Engineering Intern
   Employer: Bill Gates
   Duration: 3 Months
   Stipend: Yes ($6000)

2. Data Analyst Intern
   Employer: Jeff Bezos
   Duration: 6 Months
   Stipend: Yes ($7000)

3. Marketing Intern
   Employer: Vince McMahon
   Duration: 3 Months
   Stipend: No
```

## 🗃️ Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```
