from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime

from controllers import(
    get_all_keys,
    get_key_statuses
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
    return render_template('manage_keys.html', current_page=1, previous=previous, next = next, search = search, keyData = keyData['data'], num_pages=keyData["num_pages"], delete = ConfirmDelete, keys = keys)
