![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)

# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

The venv folder contains a virtual environment of Python 3.9.10 with all the requires packages as listed in requirements.txt preinstalled. This was necessary to do on my machine running Fedora.

However, for others this very well might be unecessary, so the venv folder can be deleted and be sure to adjust VS Code's selected interpreter to your machine's installation of Python 3.9.10, as the configuration files for this project points to venv for the default interpreter.

Changes can be made via ``CTRL + SHIFT + P``, followed by typing ``Select Interpreter`` in the search bar and choosing your installation of Python 3.9.10 when prompted. Or manually in .vscode/settings.json:

```
{
    "python.defaultInterpreterPath": "venv/bin/python",
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python-envs.pythonProjects": []
}
```

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Flask Commands

The following are the usbale Click CLI commands for this application:

```bash
flask init
```

# Database Initialization Commands

Initialize database without data
```bash
$ flask init
```

```bash
$ flask init-default
```

Initialize database with a default dataset.

As user commands require a simple 'login' to validate the existance of seperately defined users, please take note of the username and password attributes of any default accounts utilized. For newly created accounts, be sure to remember those login details as it is very much needed to use the application

```
BillGates = Employer(username="billygates", password="iLoveMicrosoft", name="Bill Gates", company="Microsoft", position="Founder")
JeffBezos = Employer(username="thereal_baldy", password="amazon123", name="Jeff Bezos", company="Amazon", position="Founder & CEO")
VinceMcMahon = Employer(username="moneybagsvince", password="wwe4life", name="Vince McMahon", company="WWE", position="Chairman & CEO")
```

```
Alice = Student(username="alice_w", password="alicepass", name="Alice Wonderland", university="Harvard University", degree="Computer Science", year=2, gpa=3.8)
Bob = Student(username="bob_b", password="bobpass", name="Bobby Brown", university="Stanford University", degree="Business Administration", year=3, gpa=3.5)
Charlie = Student(username="charlie_b", password="charliepass", name="Charlie Brown", university="MIT", degree="Mechanical Engineering", year=4, gpa=3.9)
```

```
ProfJohnson = Staff(username="prof_johnson", password="johnsonpass", name="Prof. Emily Johnson", faculty="Business")
DrLee = Staff(username="dr_lee", password="leepass", name="Dr. Michael Lee", faculty="Computer Science")
Keith = Staff(username="keith_r", password="greatistheUNC", name="Keith BaldHead RowRow", faculty="Poli-Tricks Science")
```

```
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
