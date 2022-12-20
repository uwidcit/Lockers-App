from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash

from controllers import (
    get_area_all,
    get_area_by_id,
    add_new_area,
    delete_area,
    set_description,
    set_latitude,
    set_longitude,
)

from views.forms import AreaAdd,ConfirmDelete

area_views = Blueprint('area_views', __name__, template_folder='../templates')

@area_views.route('/area', methods=['POST'])
def create_new_area():
    form = AreaAdd()
    if form.validate_on_submit:
        locker_id = request.form.get('locker_code')
        description = request.form.get('description')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')

       
        new_area = add_new_area(locker_id,description,longitude,latitude)
        
        if not new_area:
            flash("Area not created")
            return redirect(url_for('locker_views.index'))
            #jsonify({"Message": }),400
        flash("Area created")
        return redirect(url_for('locker_views.index'))

@area_views.route('/area',methods=['GET'])
def render_area_page():
    return render_template('area.html', areaData = get_area_all())

@area_views.route('/area/<id>/edit',methods=['GET'])
def render_edit_area_page(id):
    area = get_area_by_id(id)
    if not area:
        return redirect(url_for('.render_area_page'))
    
    form = AreaAdd()
    form.l_code.data = area.locker_id
    form.locker_code.data = area.id
    form.description.data = area.description
    form.latitude.data =  area.latitude
    form.longitude.data = area.longitude
    form.submit.label.text ="Update Area"

    return render_template('locker_area.html', form = form, updateMode = True)

@area_views.route('/area/<id>/update', methods=['POST'])
def update_area(id):

    area = get_area_by_id(id)
    if not area:
        flash('Area not found')
        return redirect(url_for('.render_area_page'))

    form = AreaAdd()
    if form.validate_on_submit:
        print(request.form)
        description = request.form.get('description')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')


    if area.description != description:
        if not set_description(id,description):
            flash('Error in setting description')
    if area.longitude != longitude:
        if not set_longitude (id, longitude):
            flash ("Error in processing longitude")
    if area.latitude != latitude:
        if not set_latitude (id,latitude):
            flash("Error in processing latitude")
    
    return  redirect(url_for('.render_area_page'))


@area_views.route('/area/<id>/delete', methods=['GET'])
def render_confirm_delete(id):
    area = get_area_by_id(id)

    if not area:
        flash('Area does not exist')
        return redirect(url_for('.render_area_page'))
    
    return render_template('delete_area.html',area = area, form = ConfirmDelete() )

@area_views.route('/area/<id>/confirmed', methods=['POST'])
def remove_area(id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        area = delete_area(id)

        if not area:
            flash("Area doesn't exist")
            return redirect(url_for('.render_area_page'))
        flash('Area deleted !')
    return redirect(url_for('.render_area_page'))


@area_views.route('/areas', methods=['GET'])
def get_all_areas():
    return jsonify(get_area_all()),200

@area_views.route('/area/<id>', methods=['GET'])
def get_area_id(id):
    area = get_area_by_id(id)
    if not area:
        return jsonify({"Message": "Area not found"}),404
    return jsonify(area),200


