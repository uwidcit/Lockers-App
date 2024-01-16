
from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash
from App.views.forms import  ConfirmDelete,SearchForm,LockerAdd,RentAdd,StudentAdd,TransactionAdd

from datetime import datetime
from flask_login import login_required


from App.controllers import (
    add_new_locker,
    get_locker_rent_history,
    get_area_choices,
    get_lockers_available,
    get_locker_id,
    get_locker_id_locker,
    get_all_lockers,
    update_key,
    update_locker_type,
    update_locker_status,
    swap_key,
    get_all_locker_names,
    get_all_keys_id,
    get_current_rental,
)

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')

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


@locker_views.route("/locker/<id>", methods=["GET"])
@login_required
def render_get_lockers(id):
    previous = 1 
    next = previous + 1
    locker = get_locker_id(id.upper())
    if not locker:
        flash("Locker doesn't exist")
        return redirect(url_for('.return_offline_page'))
    rents = None
    rents = get_locker_rent_history(id,2,1)
    current_rental = get_current_rental(id)
    form = LockerAdd()
    form.area.choices = get_area_choices()
    if rents:
        return render_template('lockerDetails.html', locker = locker, rents = rents['data'], previous= previous,current_page=1,next=next, locker_names= get_all_locker_names(), num_pages=rents['num_pages'],keys=get_all_keys_id(),trans=TransactionAdd(),current_rental= current_rental, form = form,delete=ConfirmDelete())
    return render_template('lockerDetails.html', locker = locker, rents = None, previous= previous,current_page=1,next=next,num_pages=1, locker_names= get_all_locker_names(),keys=get_all_keys_id(),trans=TransactionAdd(),current_rental= current_rental,form = form, delete=ConfirmDelete())

@locker_views.route("/locker/<id>/page/<offset>", methods=["GET"])
@login_required
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
        if '' in [id,locker2]:
            return jsonify({"message":"Error empty locker values"}),400
        lockers = swap_key(id, locker2)
        if lockers:
            data = []
            for l in lockers:
             data.append({
            'locker_code': l[0].locker_code,
            'locker_type':l[0].locker_type.value,
            'status': l[0].status.value,
            'area': l[0].area,
            'area_description':l[1].description
            })
            return jsonify(data),200
        return jsonify({"message":"error swapping keys"}),400

@locker_views.route('/api/locker', methods=['GET'])
@login_required
def locker_api():
    return jsonify(get_all_lockers())
    

@locker_views.route('/api/locker', methods=['POST'])
@login_required
def create_new_locker_api():
    data = request.json     #get data from JSON 
    if '' in data or data is None:
         return jsonify({"message":"Invalid values"}),400
    
    new_locker = add_new_locker(locker_code=data['locker_code'], locker_type=data['locker_type'], status=data['status'], key_id=data['key'],area=data['area'])
    if not new_locker:
        return jsonify({"message":"Locker already exist or some error has occurred"}),400
    locker = get_locker_id(data['locker_code'])
    data={
        'locker_code': locker[0].locker_code,
        'locker_type':locker[0].locker_type.value,
        'status': locker[0].status.value,
        'key':locker[0].toJSON()['key'],
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
    try:
        locker = update_locker_type(id,data['locker_type'])
        locker = update_locker_status(id,data['status'])
        update_key(id,data['key'])
    except Exception as e:
        return jsonify({"message": str(e)}),500
    locker = get_locker_id(data['locker_code'])
    locker_json={
        'locker_code': locker[0].locker_code,
        'locker_type':locker[0].locker_type.value,
        'status': locker[0].status.value,
        'key':locker[2].key_id,
        'area': locker[0].area,
        'area_description':locker[1].description
        }
    return jsonify(locker_json),200
    

@locker_views.route('/locker', methods=['GET'])
def return_offline_page():
    return send_from_directory('static', 'manage_locker_offline.html')
     