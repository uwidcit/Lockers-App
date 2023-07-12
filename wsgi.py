import click, pytest, sys
from datetime import datetime
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, add_new_locker, add_new_area, new_key, new_masterkey, new_rentType, add_new_student)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    # insert sample data into database
    create_user('rob', 'robpass')
    create_user('bob', 'bobpass')
    print('database intialized')
    add_new_area("SAC Downstairs", 12, 10)
    add_new_area("Library West(Blue)", 5, 9)
    add_new_area("SAC Female Lockers", 12, 10)

    new_masterkey("243", "Globe","Combination",datetime.now())
    
    new_key("92243", "243","Available",datetime.now())
    new_key("92301", "243","Available",datetime.now())
    new_key("92252", "243","Available",datetime.now())

    add_new_locker("A101","Medium","Free","92243",1)
    add_new_locker("A102","Medium","Free","92301",1)
    add_new_locker("A103","Medium","Free","92252",1)

    add_new_locker("S371","Medium","Free","1000",2)
    add_new_locker("S475","Small","Repair","1001",2)

    new_rentType(datetime(2022,6,1), datetime(2023,12,31), "Semester", 150)
    new_rentType(datetime(2022,6,1), datetime(2023,12,31), "Daily", 10)
    new_rentType(datetime(2022,6,1), datetime(2023,12,31), "Hourly", 2)

    add_new_student("8160666", "Kat", "Bholai", "FST","1868123456","KatBholai@gmail.com")
    add_new_student("8160777", "Jane", "Doe", "FFA","1868654321","JaneDoe@gmail.com")
    add_new_student("8160888", "John", "Doe", "LAW","1868246810","JohnDoe@gmail.com")
    
'''
User Commands
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