from flask import Blueprint, redirect, render_template, request, send_from_directory,flash,url_for,send_file
from controllers import get_current_user,export_all
import uuid
index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.app_errorhandler(400)
def render_not_found(e):
    flash('Page not found')
    print(e)
    return redirect(url_for("index_views.index_page"))


@index_views.app_errorhandler(500)
def render_not_found(e):
    flash('You did something wrong :(')
    print(e)
    return redirect(url_for("index_views.index_page"))

@index_views.route('/flaskwebgui-dumb-request-for-middleware-keeping-the-server-online', methods=['GET'])
def empty_function():
    return {},200

@index_views.route('/export',methods=['GET'])
def ex_student():
    data_list = export_all()
    data_list.seek(0)
    return send_file(data_list,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",download_name='lockers_dump_'+str(uuid.uuid4()).split("-")[0]+'.xlsx')
