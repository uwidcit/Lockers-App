from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime
from flask_login import login_required

from App.controllers import (
    get_all_masterkeys,
    new_masterkey,
    delete_masterkey,
    get_masterkey_by_id,
    get_key_masterkey_offset,
    get_key_statuses,
    new_key,
    search_masterkey,
    update_masterkey_id,
    update_series,
    update_masterkey_type
    )
from App.views.forms import SearchForm, masterKeyForm, ConfirmDelete, KeyAdd

masterkey_views = Blueprint('masterkey_views', __name__, template_folder='../templates')
page_size = 6

@masterkey_views.route('/masterkey', methods=['GET'])
@login_required
def render_masterkey_page():
    masterkeyData = get_all_masterkeys(page_size,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Master Key"
    return render_template("manage_masterkey.html", current_page =1 ,previous = previous, next = next, search=search, masterkeyData=masterkeyData["data"], keys = keys ,num_pages= masterkeyData["num_pages"], form = masterKeyForm(), delete = ConfirmDelete())

@masterkey_views.route('/masterkey', methods=['POST'])
@login_required
def create_new_masterkey():
    form = masterKeyForm()
    if form.validate_on_submit():
        masterkeyData = request.form
        if '' in masterkeyData or masterkeyData is None:
            flash("Empty values master Key not created")
            return redirect(url_for(".render_masterkey_page"))
        d_added = request.form.get('date_added')
        d_added = datetime.strptime(d_added,'%Y-%m-%d')
        masterkey = new_masterkey(masterkey_id = masterkeyData["masterkey_id"], series = masterkeyData["series"], key_type = masterkeyData["key_type"], date_added = d_added)
        if not masterkey:
            flash("Master Key not created")
            return redirect(url_for(".render_masterkey_page"))
        flash("Success")
        return redirect(url_for(".render_masterkey_page"))

@masterkey_views.route('/masterkey/<masterkey_id>/confirmed', methods=['POST'])
@login_required
def remove_master_key(masterkey_id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        masterkey = delete_masterkey(masterkey_id)
        if not masterkey:
            flash("Master Key doesn't exist")
            return redirect(url_for('.render_masterkey_page'))
        flash('Master Key deleted!')
    return redirect(url_for('.render_masterkey_page'))

@masterkey_views.route("/masterkey/<masterkey_id>/update", methods=['POST'])
@login_required
def update_masterkey(masterkey_id):
    masterkey = get_masterkey_by_id(masterkey_id)

    if not masterkey:
        flash('Master Key does not exist')
        return redirect(url_for('.render_masterkey_page'))

    form = masterKeyForm()
    if form.validate_on_submit: 
        key_type = request.form.get("key_type")
        series = request.form.get("series")
        masterkey_id_new = request.form.get("masterkey_id")

        if masterkey.key_type != key_type and key_type  is not None:
             if not update_masterkey_type(masterkey_id,key_type):
                flash("Error updating Master Key Type")
                return redirect(url_for('.render_masterkey_page'))  

        if masterkey.series != series and series is not None:
             if not update_series(masterkey_id,series):
                flash("Error updating series")
                return redirect(url_for('.render_masterkey_page'))  

        if masterkey.masterkey_id != masterkey_id_new and masterkey_id_new is not None:
            if not update_masterkey_id(masterkey_id,masterkey_id_new):
                flash("Error updating master key ID")
                return redirect(url_for('.render_masterkey_page'))  
    return redirect(url_for('.render_masterkey_page'))

@masterkey_views.route('/masterkey/page/<offset>', methods=['GET'])
@login_required
def render_masterkey_mulpages(offset):
    offset = int(offset)
    masterkeyData = get_all_masterkeys(page_size,offset)
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= masterkeyData["num_pages"]:
        next = masterkeyData["num_pages"]
    else:
        next = offset + 1
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search = SearchForm()
    search.submit.label.text = "Search Master Key"
    return render_template("manage_masterkey.html", current_page =offset ,previous = previous, next = next, search=search, keys= keys, masterkeyData=masterkeyData["data"], num_pages= masterkeyData["num_pages"], form = masterKeyForm(), delete = ConfirmDelete())

@masterkey_views.route('/masterkey/search/',methods=['GET'])
@login_required
def masterkey_search():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_masterkey(query,1,page_size)
        if result and result['data'] != []:
           num_pages = result['num_pages']
           keys = KeyAdd()
           keys.key_status.choices = get_key_statuses()
           return render_template("manage_masterkey.html", current_page =1 ,previous = previous, next = next, keys = keys, search=SearchForm(), masterkeyData=result["data"], num_pages= result["num_pages"], form = masterKeyForm(), delete = ConfirmDelete())
         
        else:
            flash('Master Key doesn''t exist')
            return redirect(url_for('.render_masterkey_page'))

@masterkey_views.route('/masterkey/search/page/<offset>',methods=['GET'])
@login_required
def masterkey_search_multi(offset):
    offset = int(offset)
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_masterkey(query,offset,page_size)
        if result:
            if offset - 1 <= 0:
                previous = 1
                offset = 1
            else:
                previous = offset - 1
            if offset + 1 >= result["num_pages"]:
                next = result["num_pages"]
            else:
                next = offset + 1
            num_pages = result["num_pages"]
            keys = KeyAdd()
            keys.key_status.choices = get_key_statuses()
            return render_template("manage_masterkey.html", current_page =offset ,previous = previous, next = next, keys = keys, search=SearchForm(), masterkeyData=result["data"], num_pages= result["num_pages"], form = masterKeyForm(), delete = ConfirmDelete())
        else:
            flash('Master Key doesn''t exist')
            return redirect(url_for('.render_masterkey_page'))

@masterkey_views.route('/masterkey/key',methods=['POST'])
@login_required
def create_key():
    form = KeyAdd()
    if form.validate_on_submit:
        key_id = request.form.get('key_id')
        masterkey_id = request.form.get('masterkey_id')
        key_status = request.form.get('key_status')
        date_added = request.form.get('date_added')
    
        url = url_for('.render_masterkey_page')
        if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')

            if callback.lower() == 'masterkey' and callback_id:
                url = url_for('.render_get_masterkey_page',id=callback_id)
            elif callback.lower()== 'key' and callback_id is None:
                url = url_for('key_views.render_keys_page')
                
        if '' in [key_id,masterkey_id,key_status,date_added]:
            flash('Key not created')
            return redirect(url) 
        
        date_added = datetime.strptime(date_added,'%Y-%m-%d')
        key = new_key(key_id,masterkey_id,key_status,date_added)

        if not key:
            flash('Key not created')
            return redirect(url) 
        else:
            flash('Success adding '+key_id)
            return redirect(url)
    flash('Something went wrong')
    return redirect(url)

@masterkey_views.route('/masterkey/<id>', methods=['GET'])
@login_required
def render_get_masterkey_page(id):
    masterkeyData = get_masterkey_by_id(id)

    if not masterkeyData:
        flash('Not found or does not exist')
        return redirect(url_for('.render_masterkey_page'))
    
    keyData = get_key_masterkey_offset(id,1,5)
    previous = 1
    next = previous + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Master Key"
    return render_template("masterkey_details.html", current_page =1 , form = masterKeyForm(),previous = previous, next = next, masterkeyData=masterkeyData, num_key= keyData['num_keys'],keyData= keyData['data'],keys = keys ,num_pages= keyData["num_pages"], delete = ConfirmDelete())

@masterkey_views.route('/masterkey/<id>/page/<offset>', methods=['GET'])
@login_required
def render_get_masterkey_page_offset(id,offset):
    offset = int(offset)
    masterkeyData = get_masterkey_by_id(id)
    if not masterkeyData:
        flash('Not found or does not exist')
        return redirect(url_for('.render_masterkey_page'))
    
    keyData = get_key_masterkey_offset(id,offset,5)
    if offset > keyData["num_pages"]:
        return redirect(url_for('.render_get_masterkey_page',id=id))
    previous = 1
    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= keyData["num_pages"]:
        next = keyData["num_pages"]
    else:
        next = offset + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Master Key"
    return render_template("masterkey_details.html", current_page = offset, form = masterKeyForm(),previous = previous, next = next, masterkeyData=masterkeyData, num_key= keyData['num_keys'],keyData= keyData['data'],keys = keys ,num_pages= keyData["num_pages"], delete = ConfirmDelete())