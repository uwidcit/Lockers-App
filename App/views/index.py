from flask import Blueprint, redirect, render_template, request, send_from_directory,flash,url_for,send_file
from App.controllers import get_current_user,export_all,import_all,delete_all,login
import uuid
import io
from flask_login import login_required
import flask_login
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

#@index_views.app_errorhandler(400)
def render_not_found(e):
    flash('Page not found')
    print(e)
    return redirect(url_for("index_views.index_page"))


#@index_views.app_errorhandler(500)
def render_not_found(e):
    flash('You did something wrong :(')
    print(e)
    return redirect(url_for("index_views.index_page"))

#@index_views.app_errorhandler(401)
def unauthorized_access(e):
    flash('You need to be logged in to see this content')
    return redirect(url_for("index_views.index_page"))

@index_views.route('/flaskwebgui-dumb-request-for-middleware-keeping-the-server-online', methods=['GET'])
def empty_function():
    return {},200

@index_views.route('/login', methods=['POST'])
def user_authen():
    data = request.form
    user = login(data['username'], data['password'])
    if user:
        flask_login.login_user(user,True)
        flash('Success')
        return redirect(url_for("locker_views.manage_locker"))
    flash('Error in credentials')
    return render_template('index.html')

@index_views.route('/logout', methods=['get'])
@login_required
def user_logout():
    flask_login.logout_user()
    return redirect(url_for("index_views.index_page"))



@index_views.route('/export',methods=['GET'])
def render_import_export():
   return render_template('export_import.html')

@index_views.route('/import',methods=['POST'])
def import_api():
   data = request.files.get('backup')

   if allowed_file(data.filename):
        data_BytesIO = io.BytesIO()
        data.save(data_BytesIO)
        import_all(data_BytesIO)
   return render_template('export_import.html')

@index_views.route('/export/file',methods=['GET'])
def ex_student():
    data_list = export_all()
    return send_file(data_list,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",as_attachment=True, attachment_filename="lockers_dump_"+str(uuid.uuid4()).split("-")[0]+".xlsx")

@index_views.route('/delete/all',methods=['GET'])
def fresh_start():
    delete_all()
    return redirect(url_for("index_views.index_page"))

@index_views.route('/offline.html',methods=['GET'])
def return_offline_page():
    return send_from_directory('static','offline.html')
