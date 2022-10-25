from flask import Blueprint, redirect, render_template, request, send_from_directory
from models import AddLocker

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/flaskwebgui-dumb-request-for-middleware-keeping-the-server-online', methods=['GET'])
def empty_function():
    return {},200

@index_views.route('/addLocker', methods=['GET'])
def addLockerPage():
    form = AddLocker()
    form.area.choices = [('1', 'FST'),('2','ENG'), ('3','FSS')]
    return render_template('addLockerForm.html', form = form)

@index_views.route('/addLocker', methods=['POST'])
def addLockerAPI():
    return {},200