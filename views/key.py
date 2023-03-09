from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime

from controllers import(
    get_all_keys,
    new_key,
    get_key_statuses,
    get_all_masterkeys_no_offset,
)

from views.forms import SearchForm, ConfirmDelete, KeyAdd

key_views = Blueprint('key_views',__name__,template_folder='../templates')

@key_views.route('/key',methods=['GET'])
def render_keys_page():
    keyData = get_all_keys(7,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    keys = KeyAdd()
    keys.key_status.choices = get_key_statuses()
    search.submit.label.text = "Search Key"
    return render_template('manage_keys.html', current_page=1, masterkeys = get_all_masterkeys_no_offset(), previous=previous, next = next, search = search, keyData = keyData['data'], num_pages=keyData["num_pages"], delete = ConfirmDelete, keys = keys)

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
