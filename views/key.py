from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime
from flask_login import login_required

from controllers import(
    get_all_keys,
    get_key_by_id,
    getKeyHistory_by_id,
    get_key_statuses,
    get_all_masterkeys_no_offset,
    get_all_locker_names,
    update_key,
    update_key_masterkey_id,
    update_key_status,

)

from views.forms import SearchForm, ConfirmDelete, KeyAdd

key_views = Blueprint('key_views',__name__,template_folder='../templates')

@key_views.route('/key',methods=['GET'])
@login_required
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
@login_required
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

@key_views.route('/key/<id>/assign',methods=['POST'])
@login_required
def assign_key_locker(id):
    form = KeyAdd()
    if form.validate_on_submit:
        locker_id = request.form.get('assign')
        locker = update_key(locker_id,id)
        url =  url_for('.render_keys_page')
        if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')

            if callback.lower() == 'key' and callback_id:
                url = url_for('.render_keyid_page',id=callback_id)
            elif callback.lower()== 'masterkey' and callback_id:
                url = url_for('masterkey_views.render_get_masterkey_page', id=callback_id)
        if not locker:
            flash('Fail assigning key to locker')
            return redirect(url)
        flash('Success')
        return redirect(url)
    
@key_views.route('/key/<id>/update',methods=['POST'])
@login_required
def update_key_data(id):
    form = KeyAdd()
    if form.validate_on_submit:
        key_id = request.form.get('key_id')
        masterkey_id = request.form.get('masterkey_id')
        key_status = request.form.get('key_status')
        date_added = datetime.strptime(request.form.get('date_added'),'%Y-%m-%d')
        key = update_key(id,key_id)
        key = update_key_status(id,key_status)
        key = update_key_masterkey_id(id,masterkey_id)

        url = url_for('masterkey_views.render_masterkey_page')
        if request.args:
            callback = request.args.get('callback')
            callback_id = request.args.get('id')

            if callback.lower() == 'masterkey' and callback_id:
                url = url_for('masterkey_views.render_get_masterkey_page',id=callback_id)
            elif callback.lower()== 'key' and not callback_id:
                url = url_for('key_views.render_keys_page')
            elif callback.lower()== 'key' and callback_id:
                url = url_for('key_views.render_keyid_page',id=callback_id)

        if not key:
            flash('Key not updated')
            return redirect(url) 
        else:
            flash('Success updating '+key_id)
            return redirect(url)
    flash('Something went wrong')
    return redirect(url)

@key_views.route('/key/<id>',methods=['GET'])
@login_required
def render_keyid_page(id):
    keyData = get_key_by_id(id)
    if not keyData:
        flash('Not found or does not exist')
        return redirect(url_for('.render_keys_page'))
    keyHistory = getKeyHistory_by_id(id,4,1)
    previous = 1
    next = previous + 1
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    return render_template('key_details.html', current_page=1, masterkeys = get_all_masterkeys_no_offset(), lockers= get_all_locker_names(), previous=previous, next = next, keyData = keyData,keyHistory=keyHistory["data"], num_pages=keyHistory["num_pages"], delete = ConfirmDelete(), keys = keys)
        
