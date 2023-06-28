from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for,flash
from flask_login import login_required

from App.controllers import (
    get_area_all,
    get_area_by_id,
    return_lockers,
    get_area_by_offset,
    get_num_area_page,
    get_locker_by_area_id_toJSON,
    add_new_area,
    delete_area,
    set_description,
    set_latitude,
    set_longitude,
    search_area,
    get_area_choices,
    get_all_keys_id
)

from App.views.forms import AreaAdd,ConfirmDelete,SearchForm,LockerAdd

area_views = Blueprint('area_views', __name__, template_folder='../templates')

@area_views.route('/area', methods=['POST'])
@login_required
def create_new_area():
    form = AreaAdd()
    if form.validate_on_submit:
        description = request.form.get('description')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')

        new_area = add_new_area(description,longitude,latitude)
        
        if not new_area:
            flash("Area not created")
            return redirect(url_for('.render_area_page'))
        flash("Area created")
        return redirect(url_for('.render_area_page'))


@area_views.route('/area',methods=['GET'])
@login_required
def render_area_page():
    num_pages = get_num_area_page(15)
    areaData = get_area_by_offset(15,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    delete = ConfirmDelete()
    return render_template('area.html', areaData = areaData,form=AreaAdd(),delete= delete,search=search,num_pages= num_pages,current_page=1, next= next, previous= previous)

@area_views.route('/area/page/<offset>',methods=['GET'])
@login_required
def render_area_page_offset(offset):
    offset = int(offset)
    num_pages = get_num_area_page(15)
    areaData = get_area_by_offset(15,offset)
    
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= num_pages:
        next = num_pages
    else:
        next = offset + 1

    search = SearchForm()
    delete = ConfirmDelete()
    return render_template('area.html', areaData = areaData,form=AreaAdd(),delete=delete,search=search,num_pages= num_pages,current_page=offset, next= next, previous= previous)

@area_views.route('/area/search/',methods=['GET'])
@login_required
def render_search_area_page():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get('search_query')
        result = search_area(query,1,15)

        if result:
            num_pages = result['num_pages']
            return render_template('area.html', areaData = result['data'],form=AreaAdd(),delete= ConfirmDelete(),search= SearchForm(),num_pages= num_pages,current_page=1, next= next, previous= previous)
        return redirect(url_for('.render_area_page'))

@area_views.route('/area/search/page/<offset>',methods=['GET'])
@login_required
def render_search_area_page_multi(offset):
    offset = int(offset)

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get('search_query')
        result = search_area(query,offset,15)

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
            return render_template('area.html', areaData = result['data'],form=AreaAdd(),delete= ConfirmDelete(),search= SearchForm(),num_pages= num_pages,current_page=offset, next= next, previous= previous)
        flash('Not found')
        return redirect(url_for('.render_area_page'))

@area_views.route('/area/<id>/update', methods=['POST'])
@login_required
def update_area(id):

    area = get_area_by_id(id)
    if not area:
        flash('Area not found')
        return redirect(url_for('.render_area_page'))

    form = AreaAdd()
    if form.validate_on_submit:
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
@login_required
def render_confirm_delete(id):
    area = get_area_by_id(id)

    if not area:
        flash('Area does not exist')
        return redirect(url_for('.render_area_page'))
    
    return render_template('delete_area.html',area = area, form = ConfirmDelete() )

@area_views.route('/area/<id>/confirmed', methods=['POST'])
@login_required
def remove_area(id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        area = delete_area(id)

        if not area:
            flash("Area doesn't exist")
            return redirect(url_for('.render_area_page'))
        flash('Area deleted !')
    return redirect(url_for('.render_area_page'))


@area_views.route('/api/area/', methods=['GET'])
@login_required
def get_all_areas():
    return jsonify(get_area_all()),200

@area_views.route('/area/<id>', methods=['GET'])
@login_required
def get_area_id(id):
    area = get_area_by_id(id)
    locker = return_lockers(id,3,1)
    previous = 1
    num_lockers = len(get_locker_by_area_id_toJSON(id))
    next = previous + 1
    form = LockerAdd()
    form.area.choices = get_area_choices()
    if not area:
        flash('Area '+id+' not found')
        return redirect(url_for('.render_area_page'))
    return render_template('get_area.html',area = area,locker=locker["data"], previous=previous,next=next,current_page=1,num_pages=locker['num_pages'],num_lockers=num_lockers,form=form,keys=get_all_keys_id())


@area_views.route('/area/<id>/page/<offset>', methods=['GET'])
@login_required
def get_area_id_multi(id,offset):
    offset = int(offset)
    area = get_area_by_id(id)
    locker = return_lockers(id,3,offset)
    num_lockers = len(get_locker_by_area_id_toJSON(id))
    form = LockerAdd()
    form.area.choices = get_area_choices()
    if not area:
        return redirect(url_for('.render_area_page'))
    
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= locker['num_pages']:
        next = locker['num_pages']
    else:
        next = offset + 1
  
    return render_template('get_area.html',area = area,locker=locker["data"], previous=previous,next=next,current_page=1,num_pages=locker['num_pages'],num_lockers=num_lockers,form=form,keys=get_all_keys_id())
