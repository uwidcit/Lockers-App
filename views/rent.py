from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify

from controllers import (
    create_rent,
    get_rent_by_id,
    get_all_rentals,
    release_rental,
    get_lockers_available,
    )

rent_views = Blueprint('rent_views', __name__, template_folder='../templates')

@rent_views.route('/rentpage',methods=['GET'])
def rent_page():
  return render_template('rent.html', results = get_all_rentals(),lockers= get_lockers_available())

@rent_views.route('/rent/add', methods=['POST'])
def create_new_rent():
    s_id = request.json.get('student_id')
    locker_id = request.json.get('locker_id')
    rentType = request.json.get('rentType')
    r_date_f = request.json.get('rent_date_from')
    r_date_t = request.json.get('rent_date_to')
    d_returned = request.json.get('date_returned')

    rental = create_rent(s_id,locker_id,rentType,r_date_f,r_date_t,d_returned)

    if not rental:
        return jsonify({"Message": "Rental not created"}),400
    return jsonify(rental.toJSON()),201

@rent_views.route('/rent/<id>', methods=['GET'])
def get_rent_id(id):
    rental = get_rent_by_id(id)

    if not rental:
        return jsonify({"Message": "Rental does not exist"}),404
    return jsonify(rental.toJSON()),200

@rent_views.route('/rent/all', methods=['GET'])
def get_all_rent(id):
    return jsonify(get_all_rentals()),200

@rent_views.route('/rent/<id>/release', methods=['PUT'])
def release_locker(id):
    #get a better way to calculate late fees 
    d_return = request.json.get('date_returned')

    rental = release_rental(id,d_return)

    if not rental:
        return jsonify({"Message": "Error releasing rental"}),400
    
    return jsonify(rental.toJSON()),200