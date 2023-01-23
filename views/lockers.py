
from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash

from views.forms import  ConfirmDelete,SearchForm,LockerAdd,RentAdd,StudentAdd


from controllers import (
    add_new_locker,
    get_area_choices,
    get_All_rentType,
    get_available_student,
    get_lockers_available,
    get_lockers_by_offset,
    get_locker_id,
    get_num_locker_page,
    get_all_lockers,
    delete_locker,
    update_key,
    search_lockers,
    update_locker_type,
    update_locker_status,
)

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')

@locker_views.route("/locker", methods=['GET'])
def manage_locker():
    num_pages = get_num_locker_page(15)
    lockerData = get_lockers_by_offset(15,1)
    previous = 1
    next = previous + 1
    form = LockerAdd()
    form.area.choices = get_area_choices()
    return render_template('manage_locker.html', lockerData=lockerData,form = form ,delete=ConfirmDelete(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=1, next= next, previous= previous)

@locker_views.route("/locker/page/<offset>", methods=['GET'])
def manage_locker_mulpages(offset):
    offset = int(offset)
    num_pages = get_num_locker_page(15)
    lockerData = get_lockers_by_offset(15,offset)

    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= num_pages:
        next = num_pages
    else:
        next = offset + 1
    form = LockerAdd()
    form.area.choices = get_area_choices()
    return render_template('manage_locker.html', lockerData=lockerData,form = form ,delete=ConfirmDelete(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=offset,next= next, previous= previous)


@locker_views.route('/locker/<id>/delete', methods=['GET'])
def render_confirm_delete(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.manage_locker'))
    
    return render_template('delete_locker.html',locker = locker, form = ConfirmDelete())

@locker_views.route("/locker/rent/<id>/student", methods=["GET"])
def select_student_page():
    studentData = get_available_student()
    search = SearchForm()
    search.submit.label.text = "Search Student"
    return render_template("manage_student.html",studentData=studentData,form=StudentAdd(),search=search)

@locker_views.route("/locker", methods=['POST'])
def add_locker():
    form = LockerAdd() # create form object
    if form.validate_on_submit:
        data = request.form # get data from form submission
        new_locker = add_new_locker(locker_code=data['locker_code'], locker_type=data['locker_type'], status=data['status'], key=data['key'],area=data['area'])
        if not new_locker:
            return redirect(url_for('.manage_locker'))
            #jsonify({"message":"Locker already exist or some error has occurred"}),400
       
    return redirect(url_for('.manage_locker'))
    #jsonify({"data":new_locker.toJSON()}),201

@locker_views.route('/locker/search',methods=['POST'])
def locker_search():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.form.get("search_query")
        result = search_lockers(query)
        if result:
           num_pages = 1
           return render_template('manage_locker.html', lockerData=result, form = LockerAdd(),delete=ConfirmDelete(), search=SearchForm(),searchMode=True, num_pages= num_pages,current_page=1, next= next, previous= previous)
         
        else:
            flash('Record doesn''t exist')
            return redirect(url_for('.manage_locker'))
        

@locker_views.route('/locker/<id>/confirmed', methods=['POST'])
def remove_area(id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        locker = delete_locker(id)
        if not locker:
            flash("Locker doesn't exist")
            return redirect(url_for('.manage_locker'))
        flash('Locker deleted !')
    return redirect(url_for('.manage_locker'))


@locker_views.route("/locker/<id>/update", methods=['POST'])
def update_lockers(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.render_area_page'))

    form = LockerAdd()
    if form.validate_on_submit: 
        locker_type = request.form.get("locker_type")
        status = request.form.get("status")
        key = request.form.get("key")

        if locker.locker_type != locker_type and locker_type  is not None:
             if not update_locker_type(id,locker_type):
                flash("Error updating LockerType")
                return redirect(url_for('.manage_locker'))  

        if locker.status != status and status is not None:
             if not update_locker_status(id,status):
                flash("Error updating status")
                return redirect(url_for('.manage_locker'))  

        if locker.key != key and key is not None:
            if not update_key(id,key):
                flash("Error updating key")
                return redirect(url_for('.manage_locker'))  

   
    return render_template('locker.html', form=form, updateMode=True)


@locker_views.route('/lockers/get/available', methods=['GET'])
def get_available_lockers():
    locker_list = get_lockers_available()

    if not locker_list:
        return jsonify({"message":"No available lockers"}),200

    return jsonify({"data":locker_list}),200

@locker_views.route('/lockers/get/<id>', methods=['GET'])
def get_id_locker(id):
    locker = get_locker_id(id)

    if not locker:
        return jsonify({"message":"Locker not found"}),404

    return jsonify({"data":locker.toJSON()}),200

@locker_views.route('/lockers/get/all',methods=['GET'])
def return_all_lockers():
    locker_list = get_all_lockers()
    if not locker_list:
        return jsonify({"error":"No lockers available"}),404
    return jsonify({"data":locker_list}),200

@locker_views.route("/locker/<id>/rent", methods=["GET"])
def render_lockers_rent(id):
    form = RentAdd()
    form.rent_type.choices = get_All_rentType()
    return render_template("addrent.html", form=form,id=id)