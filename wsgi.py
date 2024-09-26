import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import create_course, create_staff, assign_staff_to_course, view_course_staff
from App.controllers.initialize import initialize
from App.database import Course
from App.database import Staff






# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

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
Course and Staff Commands
'''
#Group for all course related commands
course_cli = AppGroup('course', help='Course and staff allocating commands')

@course_cli.command("create", help="Create a new course")
@click.argument("name")
def create_course_command(name):
    course = create_course(name)
    print(f'Created Course: "{course.name}" with ID: {course.id}')


@course_cli.command("createstaff", help= "Create a new staff member")
@click.argument("name")
@click.argument("role")
def create_staff_command(name, role):
    staff = create_staff(name, role)
    print (f'Created Staff: {staff.name}, Role: {staff.role} with ID {staff.id}')

@course_cli.command("assignstaff", help="Assign Staff to a course")
@click.argument("course_id")
@click.argument("staff_id")
def assign_staff_command(course_id, staff_id):
    # Retrieve the course and staff objects with ID
    course = Course.query.get(course_id)
    staff = Staff.query.get(staff_id)
    
    if not course:
        print(f'Course with ID {course_id} not found.')
        return
    if not staff:
        print(f'Staff with ID {staff_id} not found.')
        return
    

    success = assign_staff_to_course(course_id, staff_id)
    if success:
        print(f'Assigned Staff "{staff.name}" to Course "{course.name}"')
    else:
        print(f'Assignment Failed. Check course and staff IDs.')

@course_cli.command("viewstaff", help="View staff assigned to course")
@click.argument("course_id")
def view_staff_command(course_id):
    course = Course.query.get(course_id)  # Get the course
    if course:  # Check for course
        staff = view_course_staff(course_id)  
        if staff:
            print(f'Staff for course "{course.name}" (ID: {course_id})')  
            for s in staff:
                print(f'- {s.name}, Role: {s.role}')
        else:
            print(f'No staff found for course "{course.name}" (ID: {course_id}).')
    else:
        print(f'Course with ID {course_id} does not exist.')


app.cli.add_command(course_cli)
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