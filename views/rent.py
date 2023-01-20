from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash
from datetime import datetime
from models.rent import Status
from views.forms import SearchForm
from controllers import (
    create_rent,
    get_rent_by_id,
    get_all_rentals,
    release_rental,
    get_lockers_available,
    get_student_by_id,
    get_All_rentType,
    update_rent,
    verify_rental
    )
from views.forms import  RentAdd 

rent_views = Blueprint('rent_views', __name__, template_folder='../templates')

@rent_views.route('/rentpage',methods=['GET'])
def rent_page():
  return render_template('rent.html', results = get_all_rentals(),lockers= get_lockers_available(),search=SearchForm())

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
    rental = update_rent(id)

    if not rental:
        return jsonify({"Message": "Rental does not exist"}),404
    return jsonify(rental.toJSON()),200

@rent_views.route('/rent/all', methods=['GET'])
def get_all_rent():
    return jsonify(get_all_rentals()),200

@rent_views.route('/rent/<id>/release', methods=['GET'])
def release_locker(id):
    rental = update_rent(id)

    if not rental:
        return redirect(url_for('.rent_page'))
    
    if rental.status == Status.PAID :
        d_return = datetime.now()
        rental = release_rental(id,d_return)
    elif rental.status == Status.RETURNED:
        flash('Cannot release locker it has already been released')
        return redirect(url_for('.rent_page'))
    else:
        flash('Need to pay off balance first')
        return redirect(url_for('transactionLog_views.transactionLog_page'))
    flash('Success')
    return redirect(url_for('.rent_page'))

@rent_views.route('/rent/<id>/release/verify', methods=['GET'])
def return_locker_to_pool(id):
    rental = update_rent(id)

    if not rental:
        return redirect(url_for('.rent_page'))

    if rental.status == Status.VERIFIED:
        flash('Cannot verify locker it has already been verified')
        return redirect(url_for('.rent_page'))
    elif rental.status != Status.RETURNED:
        flash('Cannot verify locker it has already fees attached')
        return redirect(url_for('.rent_page'))
    else:
        result = verify_rental(id)
        if result:
            flash('Success')
            return redirect(url_for('.rent_page'))
        else:
            flash("An error has occured checked the logs")
            return redirect(url_for('.rent_page'))

@rent_views.route('/releasepage',methods=['GET'])
def release_page():
    rentals = get_all_rentals()
    return render_template('release.html', results = rentals)

@rent_views.route('/makerent/<id>', methods=['GET'])
def render(id):
    form = RentAdd()
    rentType_list = get_All_rentType()
    if rentType_list:
        rentType_list = [(r["id"], r["type"]+" $"+str(r["price"]) +" Yr: "+ str(r["period_from"].year) +'/'+str(r["period_from"].month) + "to" + str(r["period_to"].year) +'/'+ str(r["period_to"].month)) for r in rentType_list]
    form.rent_type.choices =  rentType_list
    return render_template('addrent.html', form=form, id = id)

@rent_views.route('/makerent/<id>', methods=['POST'])
def rent_locker(id):
    form = RentAdd() 
    
    if form.validate_on_submit:
       data = request.form 
       student = get_student_by_id(data['student_id'])
       if student:
            rent_date_from = datetime.strptime(data['rent_date_from'],'%Y-%m-%dT%H:%M')
            rent_date_to =datetime.strptime(data['rent_date_to'],'%Y-%m-%dT%H:%M')
            rental = create_rent(student_id=data['student_id'], locker_id=id,rentType=data['rent_type'],rent_date_from = rent_date_from,rent_date_to = rent_date_to)
            if rental:
                flash("Success")
            return redirect(url_for('.rent_page'))
       else:
        flash('Student doesn''t exist add them')
        return redirect(url_for('student_views.student_add')) 



