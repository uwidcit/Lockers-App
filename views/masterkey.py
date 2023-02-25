from flask import Blueprint, redirect, render_template, request, url_for, flash
from datetime import datetime

from controllers import (
    get_all_masterkeys,
    new_masterkey

    )
from views.forms import SearchForm, masterKeyForm

masterkey_views = Blueprint('masterkey_views', __name__, template_folder='../templates')

@masterkey_views.route('/masterkey', methods=['GET'])
def render_masterkey_page():
    masterkeyData = get_all_masterkeys(15,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    search.submit.label.text = "Search Master Key"
    return render_template("manage_masterkey.html", current_page =1 ,previous = previous, next = next, search=search, masterkeyData=masterkeyData["data"], num_pages= masterkeyData["num_pages"], form = masterKeyForm())

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
