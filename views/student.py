from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash

from controllers import (
    add_new_student,
    get_all_students,
    get_students_by_offset,
    get_student_by_id,
    get_student_by_id_json,
    get_rental_student,
    get_all_rentType_current,
    get_lockers_available_names,
    get_student_current_rental,
    search_student,
    update_student_id,
    update_student_first_name,
    update_student_last_name,
    update_student_phone_number,
    update_student_email,
    update_student_faculty,
    get_all_available_student

    )
from views.forms import StudentAdd, SearchForm, TransactionAdd,RentAdd

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student', methods=['POST'])
def add_student():
    form = StudentAdd()
    if form.validate_on_submit:
        data = request.form
        student = add_new_student(s_id = data['student_id'], f_name=data['f_name'], l_name=data['l_name'], faculty=data['faculty'],p_no=data['p_no'],email=data['email'])
        if not student:
            flash("Student not created")
            return redirect(url_for(".render_manage_student"))
        flash("Success")
        if request.args:
            callback = request.args.get('callback')
            return redirect(url_for('locker_views.select_student_page',id=callback))
        return redirect(url_for('.render_manage_student'))

@student_views.route('/student',methods=['GET'])
def render_manage_student():
    studentData = get_students_by_offset(15,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    search.submit.label.text = "Search Student"
    return render_template("manage_student.html",studentData=studentData["data"],num_pages= studentData["num_pages"], current_page =1 ,previous = previous, next = next , form=StudentAdd(),search=search)

@student_views.route('/student/page/<offset>',methods=['GET'])
def render_manage_student_multi():
    offset = int(offset)
    query = request.args.get('search_query')
    studentData = get_students_by_offset(15,offset)
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= studentData['num_pages']:
        next = studentData['num_pages']
    else:
        next = offset + 1
    search = SearchForm()
    search.submit.label.text = "Search Student"
    return render_template("manage_student.html",studentData=studentData["data"],num_pages= studentData["num_pages"], current_page =offset ,previous = previous, next = next , form=StudentAdd(),search=search,query=query)

@student_views.route("/student/search/",methods=['GET'])
def search_student_page():
    search = SearchForm()
    if search.validate_on_submit:
        previous = 1
        next = previous + 1
        query = request.args.get('search_query')
        student = search_student(query,15,1)
        if student:
            num_pages = student['num_pages']
            return render_template("manage_student.html",studentData=student["data"],num_pages= student["num_pages"], current_page =1 ,previous = previous, next = next , form=StudentAdd(),search=search,query=query)
        return redirect(url_for(".render_manage_student"))

@student_views.route("/student/search/page/<offset>",methods=['GET'])
def search_student_page_multi(offset):
    offset = int(offset)
    search = SearchForm()
    if search.validate_on_submit:
        query = request.args.get('search_query')
        student = search_student(query,15,1)
        if student:
            num_pages = student['num_pages']
            if offset - 1 <= 0:
                previous = 1
                offset = 1
            else:
                previous = offset - 1
        if offset + 1 >= num_pages:
            next = num_pages
        else:
            next = offset + 1
            return render_template("manage_student.html",studentData=student["data"],num_pages= student["num_pages"], current_page = offset,previous = previous, next = next , form=StudentAdd(),search=search,query=query)
        return redirect(url_for(".render_manage_student"))

@student_views.route("/student/<id>/update", methods=['POST'])
def update_student_info(id):
    student = get_student_by_id(id)

    if not student:
        flash('Student does not exist')
        return redirect(url_for('.render_manage_student'))

    form = StudentAdd()
    if form.validate_on_submit: 
        student_id = str(request.form.get("student_id"))
        f_name = str(request.form.get("f_name"))
        l_name = str(request.form.get("l_name"))
        faculty = str(request.form.get("faculty"))
        p_no  = str(request.form.get("p_no"))
        email = str(request.form.get("email"))
        
        if str(student.student_id) != student_id and student_id != "":
             if not update_student_id(id,f_name):
                flash("Error updating StudentID")
                return redirect(url_for('.render_manage_student'))  

        if student.first_name != f_name and f_name != "":
             if not update_student_first_name(id,f_name):
                flash("Error updating First Name")
                return redirect(url_for('.render_manage_student'))  

        if student.last_name != l_name and l_name != "":
            if not update_student_last_name(id,l_name):
                flash("Error updating Last Name")
                return redirect(url_for('.render_manage_student')) 
        if student.faculty != faculty and faculty != "":
             if not update_student_faculty(id,faculty):
                flash("Error updating Faculty")
                return redirect(url_for('.render_manage_student'))
        if student.phone_number != p_no and p_no != "":
             if not update_student_phone_number(id,p_no):
                flash("Error updating Phone")
                return redirect(url_for('.render_manage_student')) 
        if student.email != email and email != "":
             if not update_student_email(id,email):
                flash("Error updating Faculty")
                return redirect(url_for('.render_manage_student'))
        if request.args:
            callback = request.args.get('callback')
            return redirect(url_for('locker_views.select_student_page',id=callback))
        return redirect(url_for('.render_manage_student'))

@student_views.route('/student/<id>', methods=['GET'])
def get_student_render(id):
    result = get_student_by_id_json(id)
    
    if not result:
        return redirect(url_for(".render_manage_student"))
    rent = get_rental_student(id,5,1)
    previous = 1
    next = previous + 1
    rentForm = RentAdd()
    rentForm.student_id.name = "rent_locker_id"
    rentForm.rent_type.choices = get_all_rentType_current()
    locker_names = get_lockers_available_names()
    return render_template('studentDetails.html',student=result,rent=rent['data'],previous=previous,next=next,current_page=1,num_pages=rent['num_pages'], current_rental = get_student_current_rental(id), trans= TransactionAdd(),rentForm= rentForm,locker_names=locker_names)

@student_views.route('/student/<id>/page/<offset>', methods=['GET'])
def get_student_render_multi(id,offset):
    offset = int(offset)
    result = get_student_by_id_json(id)
    if not result:
        return redirect(url_for(".render_manage_student"))
    rent = get_rental_student(id,5,offset)
    num_pages = rent['num_pages']
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= num_pages:
        next = num_pages
    else:
        next = offset + 1
    rentForm = RentAdd()
    rentForm.student_id.name = "rent_locker_id"
    rentForm.rent_type.choices = get_all_rentType_current()
    locker_names = get_lockers_available_names()
    return render_template('studentDetails.html',student=result,rent=rent['data'],previous=previous,next=next,current_page=offset,num_pages=num_pages, current_rental = get_student_current_rental(id), trans= TransactionAdd(),rentForm= rentForm, locker_names=locker_names)

@student_views.route('/api/student/available', methods=['GET'])
def get_students_api():
    return jsonify(get_all_available_student())