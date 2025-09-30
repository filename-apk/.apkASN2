![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)

# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

The venv folder contains a virtual environment of Python 3.9.10 with all the requires packages as listed in requirements.txt preinstalled. This was necessary to do on my machine running Fedora

However, for others this very well might be unecessary, so the venv folder can be deleted and be sure to adjust VS Code's selected interpreter to your machine's installation of Python 3.9.10, as the configuration files for this project points to venv for the default interpreter

Changes can be made via ```CTRL + SHIFT + P```, followed by typing Select Interpreter in the search bar and choosing your installation of Python 3.9.10 when prompted

Or manually in .vscode/settings.json:

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

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
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
