
from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash

from views.forms import  ConfirmDelete,SearchForm,LockerAdd,RentAdd,StudentAdd,TransactionAdd

from datetime import datetime


from controllers import (
    add_new_locker,
    add_new_transaction,
    get_locker_rent_history,
    get_area_choices,
    get_All_rentType,
    get_all_rentType_tuple,
    get_all_rentType_current,
    get_available_student,
    get_lockers_available,
    get_lockers_by_offset,
    get_locker_id,
    get_locker_id_locker,
    get_num_locker_page,
    get_all_lockers,
    get_all_rentals,
    delete_locker,
    update_key,
    search_lockers,
    update_locker_type,
    update_locker_status,
)

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')

@locker_views.route("/locker", methods=['GET'])
def manage_locker():
    get_all_rentals()
    num_pages = get_num_locker_page(6)
    lockerData = get_lockers_by_offset(6,1)
    previous = 1
    next = previous + 1
    form = LockerAdd()
    form.area.choices = get_area_choices()
    return render_template('manage_locker.html', lockerData=lockerData,form = form ,delete=ConfirmDelete(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=1, next= next, previous= previous,trans=TransactionAdd())

@locker_views.route("/locker/page/<offset>", methods=['GET'])
def manage_locker_mulpages(offset):
    offset = int(offset)
    num_pages = get_num_locker_page(6)
    lockerData = get_lockers_by_offset(6,offset)

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
    return render_template('manage_locker.html', lockerData=lockerData,form = form ,delete=ConfirmDelete(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=offset,next= next, previous= previous,trans=TransactionAdd())


@locker_views.route('/locker/<id>/delete', methods=['GET'])
def render_confirm_delete(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.manage_locker'))
    
    return render_template('delete_locker.html',locker = locker, form = ConfirmDelete())

@locker_views.route("/locker/rent/<id>/student", methods=["GET"])
def select_student_page(id):
    studentData = get_available_student()
    search = SearchForm()
    rent = RentAdd()
    rent.rent_type.choices = get_all_rentType_current()
    search.submit.label.text = "Search Student"
    return render_template("locker_select_student.html",studentData=studentData,form=StudentAdd(),search=search,rent=rent,id = id)

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

@locker_views.route('/locker/search/',methods=['GET'])
def locker_search():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_lockers(query,1,6)
        if result:
           num_pages = result['num_pages']
           return render_template('manage_locker.html', lockerData=result['data'], form = LockerAdd(),delete=ConfirmDelete(), search=SearchForm(),searchMode=False,query=query ,num_pages= num_pages,current_page=1, next= next, previous= previous,trans=TransactionAdd())
         
        else:
            flash('Record doesn''t exist')
            return redirect(url_for('.manage_locker'))

@locker_views.route('/locker/search/page/<offset>/',methods=['GET'])
def locker_search_multi(offset):
    offset = int(offset)
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_lockers(query,offset,6)
        if result:
           num_pages = result['num_pages']
           if offset - 1 <= 0:
                previous = 1
                offset = 1
           else:
            previous = offset - 1
        if offset + 1 >= num_pages:
            next = num_pages
        else:
            next = offset + 1
        return render_template('manage_locker.html', lockerData=result['data'], form = LockerAdd(),delete=ConfirmDelete(), search=SearchForm(),searchMode=False,query= query, num_pages= num_pages,current_page=1, next= next, previous= previous,trans=TransactionAdd())
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
    locker = get_locker_id_locker(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.manage_locker'))

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
    return redirect(url_for('.manage_locker'))


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

@locker_views.route('/locker/<id>/transaction', methods=['POST'])
def create_new_transaction(id):
    form = TransactionAdd()
    if form.validate_on_submit:
        
        rent_id = request.form.get('rent_id')
        currency = request.form.get('currency')
        transaction_date = datetime.strptime(request.form.get('transaction_date'),'%Y-%m-%dT%H:%M')
        
        amount = request.form.get('amount')
        description = request.form.get('description')
        t_type =request.form.get('t_type')
        receipt_number = request.form.get('receipt_number')
        
        newTransaction = add_new_transaction (rent_id,currency,transaction_date,amount,description, t_type, receipt_number)
        
        if not newTransaction:
            flash('Error adding transaction')
            return redirect(url_for('.manage_locker'))
        flash('Success')
        return redirect(url_for('.manage_locker'))

@locker_views.route("/locker/<id>/rent", methods=["GET"])
def render_lockers_rent(id):
    form = RentAdd()
    form.rent_type.choices = get_All_rentType()
    return render_template("addrent.html", form=form,id=id)

@locker_views.route("/locker/<id>", methods=["GET"])
def render_get_lockers(id):
    previous = 1 
    next = previous + 1
    locker = get_locker_id(id)
    rents = get_locker_rent_history(id,2,1)
    if rents:
        return render_template('remove.html', locker = locker, rents = rents['data'], previous= previous,current_page=1,next=next,num_pages=rents['num_pages'])
    return render_template('remove.html', locker = locker, rents = None, previous= previous,current_page=1,next=next,num_pages=1)

@locker_views.route("/locker/<id>/page/<offset>", methods=["GET"])
def render_get_lockers_multi(id,offset):
    offset= int(offset)
    locker = get_locker_id(id)
    rents = get_locker_rent_history(id,2,offset)

    if rents:
        num_pages = rents['num_pages']
        if offset - 1 <= 0:
                previous = 1
                offset = 1
        else:
            previous = offset - 1
        if offset + 1 >= num_pages:
            next = num_pages
        else:
            next = offset + 1

    return render_template('remove.html', locker = locker, rents = rents['data'], num_pages=num_pages, current_page=offset, previous=previous, next=next)