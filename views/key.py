from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime

from controllers import(
    get_all_keys,
    new_key,
    get_key_statuses,
    get_all_masterkeys_no_offset,
    get_all_locker_names,
    update_key
)

from views.forms import SearchForm, ConfirmDelete, KeyAdd

key_views = Blueprint('key_views',__name__,template_folder='../templates')

@key_views.route('/key',methods=['GET'])
def render_keys_page():
    keyData = get_all_keys(6,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Key"
    return render_template('manage_keys.html', current_page=1, masterkeys = get_all_masterkeys_no_offset(), lockers= get_all_locker_names(), previous=previous, next = next, search = search, keyData = keyData['data'], num_pages=keyData["num_pages"], delete = ConfirmDelete(), keys = keys)

@key_views.route('/key/page/<offset>',methods=['GET'])
def render_keys_page_multi(offset):
    offset = int(offset)
    keyData = get_all_keys(6,offset)

    if offset - 1 <= 0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= keyData['num_pages']:
        next = keyData['num_pages']
    else:
        next = offset + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Key"
    return render_template('manage_keys.html', current_page=1, masterkeys = get_all_masterkeys_no_offset(), lockers= get_all_locker_names(), previous=previous, next = next, search = search, keyData = keyData['data'], num_pages=keyData["num_pages"], delete = ConfirmDelete(), keys = keys)

@key_views.route('/key',methods=['POST'])
def create_key():
    form = KeyAdd()
    if form.validate_on_submit:
        key_id = request.form.get('key_id')
        masterkey_id = request.form.get('masterkey_id')
        key_status = request.form.get('key_status')
        date_added = datetime.strptime(request.form.get('date_added'),'%Y-%m-%d')
        key = new_key(key_id,masterkey_id,key_status,date_added)
        if not key:
            flash('Key not created')
            return redirect(url_for('.render_keys_page')) 
        else:
            flash('Success adding '+key_id)
            return redirect(url_for('.render_keys_page'))
    flash('Something went wrong')
    return redirect(url_for('.render_keys_page'))

@key_views.route('/key/<id>/assign',methods=['POST'])
def assign_key_locker(id):
    form = KeyAdd()
    if form.validate_on_submit:
        locker_id = request.form.get('assign')
        locker = update_key(locker_id,id)
        if not locker:
            flash('Fail assigning key to locker')
            return redirect(url_for('.render_keys_page'))
        flash('Success')
        return redirect(url_for('.render_keys_page'))
        
