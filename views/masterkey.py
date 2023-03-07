from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime

from controllers import (
    get_all_masterkeys,
    new_masterkey,
    delete_masterkey,
    get_masterkey_by_id,
    get_key_statuses,
    search_masterkey,
    update_masterkey_id,
    update_series,
    update_masterkey_type
    )
from views.forms import SearchForm, masterKeyForm, ConfirmDelete, KeyAdd

masterkey_views = Blueprint('masterkey_views', __name__, template_folder='../templates')

@masterkey_views.route('/masterkey', methods=['GET'])
def render_masterkey_page():
    masterkeyData = get_all_masterkeys(15,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Master Key"
    return render_template("manage_masterkey.html", current_page =1 ,previous = previous, next = next, search=search, masterkeyData=masterkeyData["data"], keys = keys ,num_pages= masterkeyData["num_pages"], form = masterKeyForm(), delete = ConfirmDelete())

@masterkey_views.route('/masterkey', methods=['POST'])
def create_new_masterkey():
    form = masterKeyForm()
    if form.validate_on_submit():
        masterkeyData = request.form
        d_added = datetime.strptime(request.form.get('date_added'),'%Y-%m-%d')
        masterkey = new_masterkey(masterkey_id = masterkeyData["masterkey_id"], series = masterkeyData["series"], key_type = masterkeyData["key_type"], date_added = d_added)
        if not masterkey:
            flash("Master Key not created")
            return redirect(url_for(".render_masterkey_page"))
        flash("Success")
        return redirect(url_for(".render_masterkey_page"))

@masterkey_views.route('/masterkey/<masterkey_id>/confirmed', methods=['POST'])
def remove_master_key(masterkey_id):
    form = ConfirmDelete()
    if form.validate_on_submit:
        masterkey = delete_masterkey(masterkey_id)
        if not masterkey:
            flash("Master Key doesn't exist")
            return redirect(url_for('.render_masterkey_page'))
        flash('Master Key deleted !')
    return redirect(url_for('.render_masterkey_page'))

@masterkey_views.route("/masterkey/<masterkey_id>/update", methods=['POST'])
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
def render_masterkey_mulpages(offset):
    offset = int(offset)
    masterkeyData = get_all_masterkeys(15,offset)
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
def masterkey_search():
    previous = 1
    next = previous + 1

    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_masterkey(query,1,6)
        if result:
           num_pages = result['num_pages']
           keys = KeyAdd()
           keys.key_status.choices = get_key_statuses()
           return render_template("manage_masterkey.html", current_page =1 ,previous = previous, next = next, keys = keys, search=SearchForm(), masterkeyData=result["data"], num_pages= result["num_pages"], form = masterKeyForm(), delete = ConfirmDelete())
         
        else:
            flash('Master Key doesn''t exist')
            return redirect(url_for('.render_masterkey_page'))

@masterkey_views.route('/masterkey/search/page/<offset>',methods=['GET'])
def masterkey_search_multi(offset):
    offset = int(offset)
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get("search_query")
        result = search_masterkey(query,offset,6)
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
    