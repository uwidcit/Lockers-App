from models import Student
from database import db
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from controllers.log import create_log
from datetime import datetime

def add_new_student(s_id, f_name, l_name, faculty,p_no,email):
    if get_student_by_id(s_id):
        return []

    try:
        new_student = Student(s_id,f_name,l_name,faculty,p_no,email) 
        db.session.add(new_student)
        db.session.commit()
        return new_student

    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        flash("Unable to Add new Student. Check Error Log for more Details")
        db.session.rollback()
        return None

def get_student_by_id(s_id):
    student = Student.query.filter_by(student_id = s_id).first()
    if not student:
        flash("Student Does not exist.")
        return None
    return student

def get_student_by_id_json(s_id):
    student = get_student_by_id(s_id)
    if not student:
        return None
    return student.toJSON()

def update_student_id(s_id,new_s_id):
    student = get_student_by_id(s_id)

    if not student:
        return None
    
    try:
        student.student_id = new_s_id
        db.session.add(student)
        db.session.commit()

    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        flash("Unable to Update Student ID. Check Error Log for more Details")
        db.session.rollback()

def update_student_first_name(s_id, new_f_name):
    student = get_student_by_id(s_id)

    if not student:
        return None
    
    try:
        student.first_name = new_f_name
        db.session.add(student)
        db.session.commit()

    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        flash("Unable to Update Student First Name. Check Error Log for more Details")
        db.session.rollback()


def update_student_last_name(s_id, new_l_name):
    student = get_student_by_id(s_id)

    if not student:
        return None
    
    try:
        student.last_name = new_l_name
        db.session.add(student)
        db.session.commit()

    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        flash("Unable to Update Student Last Name. Check Error Log for more Details")
        db.session.rollback()
        return None

def update_student_phone_number(s_id, new_phone_no):
    student = get_student_by_id(s_id)

    if not student:
        return None
    
    try:
        student.phone_number = new_phone_no
        db.session.add(student)
        db.session.commit()

    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        flash("Unable to Update Student Phone Number. Check Error Log for more Details")
        db.session.rollback()
        return None


def update_student_email(s_id, new_email):
    student = get_student_by_id(s_id)

    if not student:
        return None
    
    try:
        student.email = new_email
        db.session.add(student)
        db.session.commit()

    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        db.session.rollback()
        return None

def update_student_faculty(s_id, new_faculty):
    student = get_student_by_id(s_id)

    if not student:
        return None
    
    try:
        student.faculty = new_faculty
        db.session.add(student)
        db.session.commit()

        
    except SQLAlchemyError as e:
        create_log(s_id, type(e), datetime.now())
        flash("Unable to Update Student Faculty.Check Error Log for more Details")
        db.session.rollback()
        return None

def get_all_students():
    students = Student.query.all()

    if not students:
        return None
    return [s.toJSON() for s in students]