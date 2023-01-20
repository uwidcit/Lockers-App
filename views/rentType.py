from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify, url_for,flash
from datetime import datetime

from controllers import (
    get_All_rentType,
    get_rentType_by_id,
    delete_rent_type,
    new_rentType,
    update_rentType_period,
    update_rentType_price,
    update_rentType_type
)

from views.forms import RentTypeAdd,ConfirmDelete,SearchForm
rentType_views = Blueprint('rentType_views', __name__, template_folder='../templates')


@rentType_views.route('/rentType',methods=['GET'])
def render_rentType_all():
    return render_template('rentType_manage.html', results=get_All_rentType(),form = RentTypeAdd(),search=SearchForm(),delete= ConfirmDelete())

@rentType_views.route('/rentType',methods=['POST'])
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
def render_confirm_delete(id):
    rentType = get_rentType_by_id(id)

    if not rentType:
        flash('Price Model does not exist')
        return redirect(url_for('.render_rentType_all'))
    
    return render_template('delete_rentType.html',rentType = rentType, form = ConfirmDelete() )

@rentType_views.route('/rentType/<id>/confirmed', methods=['POST'])
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
def update_rentType(id):
    form = RentTypeAdd()
    if form.validate_on_submit:
        rentType = get_rentType_by_id(id)

        period_from = request.form.get('period_from')
        period_to = request.form.get('period_to')
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
            if not update_rentType_price(id,price):
                flash("Error updating rentType")
            return redirect(url_for('.render_rentType_all'))

        if rentType.period != type:
            if not update_rentType_type(id,type):
                flash("Error updating rentType")
            return redirect(url_for('.render_rentType_all'))
        flash('Model changed !')
    return redirect(url_for('.render_rentType_all'))
