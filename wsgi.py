import click, pytest, sys, csv,os
from datetime import datetime
from flask import Flask
from flaskwebgui import FlaskUI
from flask.cli import with_appcontext, AppGroup
from os import path
from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, create_assistant, get_all_users_json, get_all_assistant_json,get_all_users, add_new_locker, import_all, new_key, new_masterkey, new_rentType, add_new_student)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

if __name__ == "__main__":
    FlaskUI(app=app, server="flask").run()

# This command creates and initializes or reinitializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # insert sample data into database
    print('Beginning Initalization')
    create_user('rob', 'robpass')
    create_user('bob', 'bobpass')
    create_assistant('student1','studentpass')
    print('database intialized')


@app.cli.command("restore", help="Restore DB from file in App/uploads")
def restore_db():
    print('Trying to restore')
    with open(os.path.join('App/uploads/db_restore.xlsx'),"rb") as file:
        import_all(file)
    print('Successful') 
    
'''
User Commands
'''
@app.cli.command("append", help="Appends data the database")
def append_info():
 print("Beginning Append")
 with open('keys_append.csv', mode="r") as csv_file:
    reader = csv.DictReader(csv_file)
    for r in reader:
        new_key(r["key_id"], r["masterkey_id"], r["key_status"], datetime.strptime(r['date_added'], '%Y-%m-%d'))
 with open('lockers_append.csv', mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for r in reader:
            add_new_locker(r["locker_code"],r["locker_type"],r["status"],r["key"],r["area"])
 print("Completed")

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

@user_cli.command("assistant", help="Lists assistants in the database")
@click.argument("format", default="string")
def list_user_command(format):
        print(get_all_assistant_json())

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