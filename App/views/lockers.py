
from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash,make_response

from App.views.forms import  ConfirmDelete,SearchForm,LockerAdd,RentAdd,StudentAdd,TransactionAdd

from datetime import datetime
from flask_login import login_required


from App.controllers import (
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
    swap_key,
    get_all_locker_names,
    get_all_keys_id,
    get_current_rental,
)

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')

#deprecated
#@locker_views.route("/locker", methods=['GET'])
#@login_required
def manage_locker():
    get_all_rentals()
    num_pages = get_num_locker_page(6)
    lockerData = get_lockers_by_offset(6,1)
    previous = 1
    next = previous + 1
    form = LockerAdd()
    form.area.choices = get_area_choices()
    return render_template('manage_locker.html', lockerData=lockerData,form = form ,delete=ConfirmDelete(), search=SearchForm(),keys=get_all_keys_id(), num_pages= num_pages, locker_names= get_all_locker_names(), current_page=1, next= next, previous= previous,trans=TransactionAdd())

#deprecated
#@locker_views.route("/locker/page/<offset>", methods=['GET'])
#@login_required
def manage_locker_mulpages(offset):
    get_all_rentals()
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
    return render_template('manage_locker.html', lockerData=lockerData,form = form ,delete=ConfirmDelete(), search=SearchForm(),keys=get_all_keys_id(), num_pages= num_pages,locker_names= get_all_locker_names(), current_page=offset,next= next, previous= previous,trans=TransactionAdd())

#deprecated
#@locker_views.route('/locker/<id>/delete', methods=['GET'])
#@login_required
def render_confirm_delete(id):
    locker = get_locker_id(id)

    if not locker:
        flash('Locker does not exist')
        return redirect(url_for('.manage_locker'))
    
    return render_template('delete_locker.html',locker = locker, form = ConfirmDelete())

#deprecated
#@locker_views.route("/locker/rent/<id>/student", methods=["GET"])
#@login_required
def select_student_page(id):
    studentData = get_available_student(8,1)
    search = SearchForm()
    rent = RentAdd()
    previous = 1
    next = previous + 1
    rent.rent_type.choices = get_all_rentType_current()
    search.submit.label.text = "Search Student"
    return render_template("locker_select_student.html",studentData=studentData['data'],num_pages=studentData["num_pages"], form=StudentAdd(),search=search,rent=rent,id = id,current_page=1, next= next, previous= previous)

#deprecated
#@locker_views.route("/locker/rent/<id>/student/<offset>", methods=["GET"])
def select_student_page_multi(id,offset):
    offset = int(offset)
    studentData = get_available_student(8,offset)

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
    rent = RentAdd()
    rent.rent_type.choices = get_all_rentType_current()
    search.submit.label.text = "Search Student"
    return render_template("locker_select_student.html",studentData=studentData['data'],num_pages=studentData["num_pages"], form=StudentAdd(),search=search,rent=rent,id = id,current_page=offset,next= next, previous= previous)

#deprecated
#@locker_views.route("/locker", methods=['POST'])
#@login_required
def add_locker():
    form = LockerAdd() # create form object
    if form.validate_on_submit:
        data = request.form # get data from form submission
        new_locker = add_new_locker(locker_code=data['locker_code'], locker_type=data['locker_type'], status=data['status'], key_id=data['key'],area=data['area'])
        url = url_for('.manage_locker')
        if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')
            if callback.lower() == 'area':
                url = url_for('area_views.get_area_id',id=callback_id)

        if not new_locker:
            return redirect(url)
            #jsonify({"message":"Locker already exist or some error has occurred"}),400
    
    return redirect(url)
    #jsonify({"data":new_locker.toJSON()}),201

#deprecated
#@locker_views.route('/locker/search/',methods=['GET'])
#@login_required
def locker_search():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_lockers(query,1,6)
        if result:
           num_pages = result['num_pages']
           return render_template('manage_locker.html', lockerData=result['data'], form = LockerAdd(),delete=ConfirmDelete(), search=SearchForm(),keys=get_all_keys_id(),query=query ,num_pages= num_pages,locker_names= get_all_locker_names(), current_page=1, next= next, previous= previous,trans=TransactionAdd())
         
        else:
            flash('Record doesn''t exist')
            return redirect(url_for('.manage_locker'))
#deprecated
#@locker_views.route('/locker/search/page/<offset>/',methods=['GET'])
#@login_required
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
        return render_template('manage_locker.html', lockerData=result['data'], form = LockerAdd(),delete=ConfirmDelete(), search=SearchForm(),keys=get_all_keys_id(),query= query, num_pages= num_pages, locker_names = get_all_locker_names(), current_page=1, next= next, previous= previous,trans=TransactionAdd())
    else:
        flash('Record doesn''t exist')
        return redirect(url_for('.manage_locker'))

#deprecated
#@locker_views.route('/locker/<id>/confirmed', methods=['POST'])
#@login_required
def remove_area(id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        locker = delete_locker(id)
        if not locker:
            flash("Locker doesn't exist")
            return redirect(url_for('.manage_locker'))
        flash('Locker deleted !')
    return redirect(url_for('.manage_locker'))

#deprecated
#@locker_views.route("/locker/<id>/update", methods=['POST'])
#@login_required
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
@login_required
def get_available_lockers():
    locker_list = get_lockers_available()

    if not locker_list:
        return jsonify({"message":"No available lockers"}),200

    return jsonify({"data":locker_list}),200

@locker_views.route('/lockers/get/<id>', methods=['GET'])
@login_required
def get_id_locker(id):
    locker = get_locker_id(id)

    if not locker:
        return jsonify({"message":"Locker not found"}),404

    return jsonify({"data":locker.toJSON()}),200

#deprecated
#@locker_views.route('/locker/<id>/transaction', methods=['POST'])
#@login_required
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
        
        url = url_for('.manage_locker')

        if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')

            if callback.lower() == 'rent':
                url = url_for('rent_views.get_rent_id',id=callback_id)
            elif callback.lower() == 'locker':
                url = url_for('locker_views.render_get_lockers',id=callback_id)

        if not newTransaction:
            flash('Error adding transaction')
            return redirect(url)
        flash('Success')
        return redirect(url)

#deprecated
#@locker_views.route("/locker/<id>/rent", methods=["GET"])
#@login_required
def render_lockers_rent(id):
    form = RentAdd()
    form.rent_type.choices = get_All_rentType()
    return render_template("addrent.html", form=form,id=id)

#deprecated
#@locker_views.route("/locker/<id>", methods=["GET"])
#@login_required
def render_get_lockers(id):
    previous = 1 
    next = previous + 1
    locker = get_locker_id(id)
    rents = get_locker_rent_history(id,2,1)
    current_rental = get_current_rental(id)
    form = LockerAdd()
    form.area.choices = get_area_choices()
    if rents:
        return render_template('lockerDetails.html', locker = locker, rents = rents['data'], previous= previous,current_page=1,next=next, locker_names= get_all_locker_names(), num_pages=rents['num_pages'],keys=get_all_keys_id(),trans=TransactionAdd(),current_rental= current_rental, form = form,delete=ConfirmDelete())
    return render_template('lockerDetails.html', locker = locker, rents = None, previous= previous,current_page=1,next=next,num_pages=1, locker_names= get_all_locker_names(),keys=get_all_keys_id(),trans=TransactionAdd(),current_rental= current_rental,form = form, delete=ConfirmDelete())
#deprecated
#@locker_views.route("/locker/<id>/page/<offset>", methods=["GET"])
#@login_required
def render_get_lockers_multi(id,offset):
    offset= int(offset)
    locker = get_locker_id(id)
    rents = get_locker_rent_history(id,2,offset)
    current_rental = get_current_rental(id)
    form = LockerAdd()
    form.area.choices = get_area_choices()

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
    return render_template('remove.html', locker = locker, rents = rents['data'], num_pages=num_pages, current_page=offset, locker_names= get_all_locker_names(), previous=previous, next=next,keys=get_all_keys_id(),current_rental= current_rental, form = form,delete=ConfirmDelete())

@locker_views.route('/api/locker/swap', methods=['PUT'])
@login_required
def switch_key():
        locker2 = request.json.get("locker_code2")
        id = request.json.get("locker_code1")
        locker1 = swap_key(id, locker2)
        if locker1:
            return jsonify(locker1.toJSON()),200
        return jsonify({"message":"error swapping keys"}),400

@locker_views.route('/api/locker', methods=['GET'])
@login_required
def locker_api():
    return jsonify(get_all_lockers())

@locker_views.route('/api/locker', methods=['POST'])
@login_required
def create_new_locker_api():
    data = request.json     #get data from JSON 
    new_locker = add_new_locker(locker_code=data['locker_code'], locker_type=data['locker_type'], status=data['status'], key_id=data['key'],area=data['area'])
    if not new_locker:
        return jsonify({"message":"Locker already exist or some error has occurred"}),400
    locker = get_locker_id(data['locker_code'])
    data={
        'locker_code': locker[0].locker_code,
        'locker_type':locker[0].locker_type.value,
        'status': locker[0].status.value,
        'key':locker[0].key,
        'area': locker[0].area,
        'area_description':locker[1].description
        }
    return jsonify(data),201

@locker_views.route('/api/locker', methods=['PUT'])
@login_required
def update_locker_api():
    data = request.json 
    locker = get_locker_id_locker(data['locker_code'])
    if not locker:
        return jsonify({"message": "Locker does not exist"}),404
    id = data['locker_code']
    if locker.locker_type != data['locker_type'] and data['locker_type']  is not None:
        if not update_locker_type(id,data['locker_type']):
            return jsonify({"message": "Error updating locker type"}),500
    
    if locker.status != data['status'] and data['status'] is not None:
        if not update_locker_status(id,data['status']):
            return jsonify({"message": "Error updating status"}),500

    if locker.key != data['key'] and data['key'] is not None:
        if not update_key(id,data['key']):
            return jsonify({"message": "Error updating key"}),500
    locker = get_locker_id(data['locker_code'])
    locker_json={
        'locker_code': locker[0].locker_code,
        'locker_type':locker[0].locker_type.value,
        'status': locker[0].status.value,
        'key':locker[0].key,
        'area': locker[0].area,
        'area_description':locker[1].description
        }
    return jsonify(locker_json),200
    

@locker_views.route('/locker', methods=['GET'])
def return_offline_page():
    get_all_rentals()
    return send_from_directory('static', 'manage_locker_offline.html')
     