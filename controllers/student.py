from database import db
from models import Student
from sqlalchemy.exc import SQLAlchemyError

def add_student(student_id, first_name, last_name, faculty,phone_number,email):
    try:
        new_student = Student(student_id, first_name,last_name, faculty,phone_number,email)
        db.session.add(new_student)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_student(id):
    student = Student.query.filter_by(id = id).first()

    if not student:
        return []

    return student

def get_student_json(id):
    student = get_student(id)

    if not student:
        return []

    return student.toJSON()

def update_student(id,first_name, last_name, faculty,phone_number,email):
    student = get_student(id)

    if not student:
        return []

    if first_name != "":
        student.first_name = first_name
    if last_name != "":
        student.last_name = last_name
    if faculty != "":
        student.faculty = faculty
    if phone_number != "":
        student.phone_number = phone_number
    if email != "":
        student.email = email
    
    try:
        db.session.add(student)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return []
    

def get_all_students():
    students = Student.query.all()

    if not students:
        return []

    return [s.toJSON for s in students]

