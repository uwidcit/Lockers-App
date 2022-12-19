from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for

from controllers import (
    create_rent,
    get_rent_by_id,
    get_all_rentals,
    get_all_rented,
    release_rental,
    get_lockers_available,
    )
from forms import TransactionAdd, RentAdd 

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

@rent_views.route('/rent/<id>/release', methods=['GET'])
def render_release_locker(id):
    #get a better way to calculate late fees 
   return render_template('release_transaction.html', form=TransactionAdd())
@rent_views.route('/rent/<id>/release', methods=['PUT'])
def release_locker(id):
    #get a better way to calculate late fees 
    d_return = request.json.get('date_returned')

    rental = release_rental(id,d_return)

    if not rental:
        return jsonify({"Message": "Error releasing rental"}),400
    
    return jsonify(rental.toJSON()),200

@rent_views.route('/releasepage',methods=['GET'])
def release_page():
    rentals = get_all_rented()
    rentals = [r.toJSON for r in rentals]
    return render_template('release.html', results = rentals)

@rent_views.route('/makerent/<id>', methods=['GET'])
def render(id):
    form = RentAdd()
    return render_template('addrent.html', form=form, id = id)

@rent_views.route('/makerent/<id>', methods=['POST'])
def rent_locker(id):
    form = RentAdd()
    #get a better way to calculate late fees 
    data = request.form
    rental = create_rent(student_id=data['student_id'], locker_id=id,rentType=data['rent_type'], rent_date_from=data['rent_date_from'], rent_date_to=data['rent_date_to'],date_returned =  "2018-12-19 09:26:03.478039")

    if not rental:
        return redirect(url_for('rent_views.render', id = id))
    
    return jsonify(rental.toJSON()),200
    return redirect(url_for('.student_add',id =id, student_id=student_id))




@rent_views.route('/makerent/<id>/<student_id>', methods=['GET'])
def student_add(id,student_id):
    form = StudentAdd()
    return render_template('student.html', form=form, id = id, student_id=student_id)

@rent_views.route('/makerent/<id>/<student_id>', methods=['POST'])
def add_student(id,student_id):
    form = StudentAdd()
    #get a better way to calculate late fees 
    data = request.form
    student = add_new_student(s_id = data['student_id'], f_name=data['f_name'], l_name=data['l_name'], faculty=data['faculty'],p_no=data['p_no'],email=data['email'])
    if not student:
        return redirect(url_for('rent_views.render', id = id))
    

    return redirect(url_for('rent_views.render', id = id))