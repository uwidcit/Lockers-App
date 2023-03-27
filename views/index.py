from flask import Blueprint, redirect, render_template, request, send_from_directory,flash,url_for,send_file
from controllers import get_current_user,export_all,import_all
import uuid
import io
index_views = Blueprint('index_views', __name__, template_folder='../templates')

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    data_list.seek(0)
    return send_file(data_list,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",as_attachment=True, attachment_filename="lockers_dump_"+str(uuid.uuid4()).split("-")[0]+".xlsx")
