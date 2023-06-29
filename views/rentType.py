from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify, url_for,flash
from datetime import datetime
from flask_login import login_required

from controllers import (
    get_All_rentType,
    get_rentType_by_id,
    delete_rent_type,
    get_rentType_by_offset,
    new_rentType,
    search_rentType,
    update_rentType_period,
    update_rentType_price,
    update_rentType_type
)

from views.forms import RentTypeAdd,ConfirmDelete,SearchForm
rentType_views = Blueprint('rentType_views', __name__, template_folder='../templates')


@rentType_views.route('/rentType',methods=['GET'])
@login_required
def render_rentType_all():
    data = get_rentType_by_offset(15,1)
    num_pages = data['num_pages']
    previous = 1
    next = previous + 1
    return render_template('rentType_manage.html', results=data['data'],form = RentTypeAdd(),search=SearchForm(),delete= ConfirmDelete(), previous= previous, next= next, current_page=1,num_pages=num_pages)

@rentType_views.route('/rentType/page/<offset>',methods=['GET'])
@login_required
def render_rentType_all_multi(offset):
    int(offset)
    data = get_rentType_by_offset(15,offset)
    num_pages = data['num_pages']
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= num_pages:
        next = num_pages
    else:
        next = offset + 1

    return render_template('rentType_manage.html', results=data['data'],form = RentTypeAdd(),search=SearchForm(),delete= ConfirmDelete(), previous= previous, next= next, current_page=offset)

@rentType_views.route('/rentType',methods=['POST'])
@login_required
def create_new_rentType():
    form = RentTypeAdd()

    if form.validate_on_submit:
        period_from = datetime.strptime(request.form.get('period_from'), '%Y-%m-%d')
        period_to = datetime.strptime(request.form.get('period_to'), '%Y-%m-%d')
        type =  request.form.get('type')
        price = request.form.get('price')

        print(period_from)
        rentType = new_rentType(period_from, period_to,type,price)

        if not rentType:
            flash('Error in creation')
            return redirect(url_for('.render_rentType_new'))
        flash('Success')
        return redirect(url_for('.render_rentType_all'))
        

@rentType_views.route('/rentType/<id>/delete', methods=['GET'])
@login_required
def render_confirm_delete(id):
    rentType = get_rentType_by_id(id)

    if not rentType:
        flash('Price Model does not exist')
        return redirect(url_for('.render_rentType_all'))
    
    return render_template('delete_rentType.html',rentType = rentType, form = ConfirmDelete() )

@rentType_views.route('/rentType/<id>/confirmed', methods=['POST'])
@login_required
def remove_area(id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        rentType = delete_rent_type(id)

        if rentType is None:
            flash("Model doesn't exist or a Rental exists with this model that cannot be deleted")
            return redirect(url_for('.render_rentType_all'))
        flash('Model deleted !')
    return redirect(url_for('.render_rentType_all'))

@rentType_views.route('/rentType/<id>/edit', methods=['GET'])
@login_required
def render_edit_pade(id):
    rentType = get_rentType_by_id(id)

    if not rentType:
        flash('Price Model does not exist')
        return redirect(url_for('.render_rentType_all'))
    form = RentTypeAdd()
    
    form.period_from.data = rentType.period_from
    form.period_to.data = rentType.period_to
    form.price.data = rentType.price
    form.type.data = rentType.type
    return render_template('rentType.html',updateMode = True, id= id, form = form)

@rentType_views.route('/rentType/<id>/update', methods=['POST'])
@login_required
def update_rentType(id):
    form = RentTypeAdd()
    if form.validate_on_submit:
        rentType = get_rentType_by_id(id)

        period_from = datetime.strptime(request.form.get('period_from'),'%Y-%m-%d') 
        period_to = datetime.strptime(request.form.get('period_to'),'%Y-%m-%d') 

        type = request.form.get('type')
        price = request.form.get('price')

        
        if rentType is None:
            flash("Model doesn't exist or a Rental exists with this model that cannot be altered")
            return redirect(url_for('.render_rentType_all'))
        
        
        if rentType.period_from != period_from or rentType.period_to != period_to:
            if not update_rentType_period(id,period_from,period_to):
                flash("Error updating rentType")
                return redirect(url_for('.render_rentType_all'))
        
        if rentType.price != price:
            print("yes")
            if not update_rentType_price(id,price):
                flash("Error updating rentType")
                return redirect(url_for('.render_rentType_all'))

        if rentType.type != type:
            if not update_rentType_type(id,type):
                flash("Error updating rentType")
                return redirect(url_for('.render_rentType_all'))
        flash('Model changed !')
    return redirect(url_for('.render_rentType_all'))

@rentType_views.route('/rentType/search',methods=['GET'])
@login_required
def search_rentTypes():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        data = search_rentType(query,15,1)

        if data:
             num_pages = data['num_pages']
             return render_template('rentType_manage.html', results=data['data'],form = RentTypeAdd(),search=SearchForm(),delete= ConfirmDelete(), previous= previous, next= next, current_page=1,num_pages=num_pages)
    return redirect(url_for('.render_rentType_all'))

@rentType_views.route('/rentType/search/page/<offset>/',methods=['GET'])
@login_required
def search_rentTypes_multi(offset):
    offset = int(offset)

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        data = search_rentType(query,15,offset)

        if data:
             num_pages = data['num_pages']
             if offset - 1 <= 0:
                previous = 1
                offset = 1
             else:
                previous = offset - 1
        if offset + 1 >= num_pages:
            next = num_pages
        else:
            next = offset + 1
        return render_template('rentType_manage.html', results=data['data'],form = RentTypeAdd(),search=SearchForm(),delete= ConfirmDelete(), previous= previous, next= next, current_page=offset,num_pages=num_pages)
    return redirect(url_for('.render_rentType_all'))

@rentType_views.route('/api/rentType',methods=['GET'])
@login_required
def api_getRentTypes():
    rentTypes = get_All_rentType()
    if not rentTypes: 
        return {}
    return jsonify(rentTypes),200