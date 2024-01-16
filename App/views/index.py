from flask import Blueprint, redirect, render_template, request, current_app as app,send_from_directory,flash,url_for,send_file
from App.database import db
from App.controllers import export_all,login
import uuid
from flask_login import login_required
from sqlalchemy import exc
import flask_login
from App.views.admin import admin_only
import os
from os import path
index_views = Blueprint('index_views', __name__, template_folder='../templates')

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@index_views.route('/', methods=['GET'])
def index_page():
    if not flask_login.current_user.is_anonymous:
        return redirect(url_for("locker_views.return_offline_page"))
    return render_template('index.html')

@index_views.app_errorhandler(400)
def render_not_found(e):
    flash('Page not found')
    return redirect(url_for("index_views.index_page"))

@index_views.app_errorhandler(403)
def render_not_found(e):
    flash('Administative account required')
    return redirect(url_for("locker_views.return_offline_page"))

@index_views.app_errorhandler(exc.SQLAlchemyError)
def rollback_db(e):
    db.session.rollback()
    #return redirect(url_for("locker_views.return_offline_page"))

@index_views.app_errorhandler(401)
def unauthorized_access(e):
    flash('You need to be logged in to see this content')
    return redirect(url_for("index_views.index_page"))

@index_views.route('/flaskwebgui-dumb-request-for-middleware-keeping-the-server-online', methods=['GET'])
def empty_function():
    return {},200

@index_views.route('/unauthorized', methods=['GET'])
def unauthorized_page():
    return render_template('adminOnly.html')

@index_views.route('/login', methods=['POST'])
def user_authen():
    data = request.form
    user = login(data['username'], data['password'])
    if user:
        flask_login.login_user(user,True)
        flash('Success')
        return redirect(url_for("locker_views.return_offline_page"))
    flash('Error in credentials')
    return render_template('index.html')

@index_views.route('/logout', methods=['get'])
@login_required
def user_logout():
    flask_login.logout_user()
    return redirect(url_for("index_views.index_page"))



@index_views.route('/export',methods=['GET'])
@admin_only
def render_import_export():
   return render_template('export_import.html')

@index_views.route('/import',methods=['POST'])
@admin_only
def import_api():
   data = request.files.get('backup')
   if allowed_file(data.filename):
        filename = 'db_restore.xlsx'
        if not os.path.isdir(app.config['UPLOADED_PHOTOS_DEST']):
            os.mkdir(os.path.join(app.config['UPLOADED_PHOTOS_DEST']))
        data.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
   return render_template('export_import.html')

@index_views.route('/export/file',methods=['GET'])
@admin_only
def ex_student():
    data_list = export_all()
    return send_file(data_list,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",as_attachment=True, attachment_filename="lockers_dump_"+str(uuid.uuid4()).split("-")[0]+".xlsx")

@index_views.route('/offline.html',methods=['GET'])
def return_offline_page():
    return send_from_directory('static','offline.html')
