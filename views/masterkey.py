from flask import Blueprint, redirect, render_template, request, url_for, flash

from controllers import (
    get_all_masterkeys,

    )
from views.forms import SearchForm

masterkey_views = Blueprint('masterkey_views', __name__, template_folder='../templates')

@masterkey_views.route('/masterkey', methods=['GET'])
def render_masterkey_page():
    masterkeyData = get_all_masterkeys(15,1)
    previous = 1
    next = previous + 1
    search = SearchForm()
    search.submit.label.text = "Search Master Key"
    return render_template("manage_masterkey.html", current_page =1 ,previous = previous, next = next, search=search)
