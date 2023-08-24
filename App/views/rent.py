from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash
from datetime import datetime
from App.models.rent import RentStatus as Status
from App.views.forms import SearchForm
from App.controllers import (
    create_rent,
    create_comment,
    get_all_rentType_tuple,
    get_transactions,
    get_all_rentals,
    get_comments_offset,
    release_rental,
    release_locker,
    get_lockers_available,
    get_student_by_id,
    get_All_rentType,
    update_rent,
    verify_rental
    )
from App.views.forms import  RentAdd, TransactionAdd
from flask_login import login_required

rent_views = Blueprint('rent_views', __name__, template_folder='../templates')

@rent_views.route('/rentpage',methods=['GET'])
def rent_page():
  return render_template('rent.html', lockers= get_lockers_available(),search=SearchForm())


@rent_views.route('/rentpage/search',methods=['POST'])
def rent_search():
    form = SearchForm()
    if form.validate_on_submit:
        query = request.form.get("search_query")
        result = get_locker_id(query)
        if result:
           return render_template('rent.html', lockers=[result], search=SearchForm()) 
        else:
            flash('Record doesn''t exist')
            return redirect(url_for('.rent_page'))
@rent_views.route('/api/locker/rent', methods=['POST'])
@login_required
def create_new_rent():
    s_id = request.json.get('student_id')
    locker_id = request.json.get('locker_id')
    rentType = request.json.get('rentType')
    rent_method = request.json.get('rentMethod')
    print(rent_method)
    r_date_f = datetime.strptime(request.json.get('rent_date_from'),'%Y-%m-%dT%H:%M')
    r_date_t = datetime.strptime(request.json.get('rent_date_to'),'%Y-%m-%dT%H:%M')
    rental = create_rent(s_id,locker_id,rentType,r_date_f,r_date_t,rent_method)
    if not rental:
        return jsonify({"Message": "Rental not created"}),400
    return jsonify(rental.toJSON()),201

@rent_views.route('/rent/<id>', methods=['GET'])
@login_required
def get_rent_id(id):
    rental = update_rent(id)
    transaction = get_transactions(id,5,1)

    previous = 1
    next = previous + 1

    if not rental:
        return redirect(url_for('locker_views.manage_locker'))
    return render_template('addrent.html', rent = rental,transaction=transaction['data'], current_page=1,next=next,previous=previous,num_pages=transaction['num_pages'],trans = TransactionAdd())

@rent_views.route('/rent/<id>/page/<offset>', methods=['GET'])
@login_required
def get_rent_id_multi(id,offset):
    offset = int(offset)
    rental = update_rent(id)

    if not rental:
        return redirect(url_for('locker_views.manage_locker'))

    transaction = get_transactions(id,5,offset)
    if transaction:
        num_pages = transaction['num_pages']
        if offset - 1 <= 0:
                previous = 1
                offset = 1
        else:
            previous = offset - 1
        if offset + 1 >= num_pages:
            next = num_pages
        else:
            next = offset + 1
    return render_template('addrent.html', rent = rental,transaction=transaction['data'], current_page=offset,next=next,previous=previous,num_pages=transaction['num_pages'])

@rent_views.route('/rent/all', methods=['GET'])
@login_required
def get_all_rent():
    return jsonify(get_all_rentals()),200

@rent_views.route('/rent/<id>/release', methods=['GET'])
@login_required
def release_locker(id):
    rental = update_rent(id)
    url = url_for('locker_views.return_offline_page')
    if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')
            if callback.lower() == 'rent':
                url = url_for('.get_rent_id',id=callback_id)
            elif callback.lower() == 'student':
                url = url_for('student_views.get_student_render',id=callback_id)
    if not rental:
        return redirect(url)
    
    if rental.status == Status.PAID :
        d_return = datetime.now()
        d_return.replace(second=0,microsecond=0)
        rental = release_rental(id,d_return)
    elif rental.status == Status.RETURNED:
        flash('Cannot release locker it has already been released')
        return redirect(url)
    else:
        flash('Need to pay off balance first')
        return redirect(url)
    flash('Success')
    return redirect(url)

@rent_views.route('/rent/<id>/release/verify', methods=['GET'])
@login_required
def return_locker_to_pool(id):
    rental = update_rent(id)

    url = url_for('locker_views.return_offline_page')
    if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')
            if callback.lower() == 'rent':
                url = url_for('.get_rent_id',id=callback_id)
            elif callback.lower() == 'student':
                url = url_for('student_views.get_student_render',id=callback_id)
    if not rental:
        return redirect(url)

    if rental.status == Status.VERIFIED:
        result = verify_rental(id)
        flash('Cannot verify locker it has already been verified')
        return redirect(url)
    elif rental.status != Status.RETURNED:
        flash('Cannot verify locker it has already fees attached')
        return redirect(url)
    else:
        result = verify_rental(id)
        if result:
            flash('Success')
            return redirect(url)
        else:
            flash("An error has occured checked the logs")
            return redirect(url)

@rent_views.route('/api/rent/<id>/notes',methods=['GET'])
@login_required
def notes_api(id):
    notes = get_comments_offset(id,3,1)
    return jsonify(notes),200


@rent_views.route('/api/rent/<id>/notes/<offset>',methods=['GET'])
@login_required
def notes_api_multi(id,offset):
    offset = int(offset)
    notes = get_comments_offset(id,3,offset)
    return jsonify(notes),200

@rent_views.route('/api/rent/<id>/notes',methods=['POST'])
@login_required
def new_note_api(id):
    data = request.json
    new_comment = create_comment(id,data['comment'],datetime.now().date())

    if new_comment:
        return jsonify(new_comment.toJSON(),200)

    return jsonify({'error':'Not created'}),400

@rent_views.route('/makerent/<id>', methods=['GET'])
@login_required
def render(id):
    form = RentAdd()
    rentType_list = get_All_rentType()
    if rentType_list:
        rentType_list = get_all_rentType_tuple()
    form.rent_type.choices =  rentType_list
    return render_template('addrent.html', form=form, id = id)

@rent_views.route('/makerent/<id>', methods=['POST'])
@login_required
def rent_locker(id):
    form = RentAdd() 
    
    if form.validate_on_submit:
       data = request.form 
       student = get_student_by_id(data['student_id'])
       if student:
            rent_date_from = datetime.strptime(data['rent_date_from'],'%Y-%m-%dT%H:%M')
            rent_date_to =datetime.strptime(data['rent_date_to'],'%Y-%m-%dT%H:%M')
            if rent_date_to <= rent_date_from:
                return redirect(url_for('locker_views.manage_locker'))
            rental = create_rent(student_id=data['student_id'], locker_id=id,rentType=data['rent_type'],rent_date_from = rent_date_from,rent_date_to = rent_date_to)
            if rental:
                flash("Success")
            return redirect(url_for('locker_views.manage_locker'))
       else:
        flash('Student doesn''t exist add them')
        return redirect(url_for('student_views.student_add')) 


@rent_views.route('/makerent/student/<student_id>', methods=['POST'])
@login_required
def rent_locker_student(student_id):
    form = RentAdd() 
    if form.validate_on_submit:
       data = request.form 
       student = get_student_by_id(student_id)

       url = url_for('locker_views.manage_locker')
    
       if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')
            if callback.lower() == 'student':
                url = url_for('student_views.get_student_render', id=callback_id)

       if student:
            locker = data['rent_locker_id']
            rent_date_from = datetime.strptime(data['rent_date_from'],'%Y-%m-%dT%H:%M')
            rent_date_to =datetime.strptime(data['rent_date_to'],'%Y-%m-%dT%H:%M')
            if rent_date_to <= rent_date_from:
                return redirect(url)
            rental = create_rent(student_id=student_id,locker_id=locker,rentType=data['rent_type'],rent_date_from = rent_date_from,rent_date_to = rent_date_to)
            if rental:
                flash("Success")
            return redirect(url)
       else:
        flash('Student doesn''t exist add them')
        return redirect(url)


