from flask import Blueprint, render_template, jsonify, request, send_from_directory,send_file,current_app,make_response,redirect,url_for,flash
from flask_login import login_required, current_user
from App.views.admin import admin_only


from App.controllers import (
    create_user, 
    create_assistant,
    change_password,
    set_assistant_password,
    delete_assistant,
    get_all_users,
    get_all_users_json,
    store_file,
    get_all_assistant_by_offset,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')
size = 6
@user_views.route('/upload', methods=['POST'])
def upload_file_route():
    user_file = request.files.getlist('upload')

    for f in user_file:
        store_file(f)
    return []

@user_views.route('/users', methods=['GET'])
@login_required
@admin_only
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users/password', methods=['GET'])
@login_required
def get_password_page():
    return render_template('account.html')

@user_views.route('/users/password', methods=['POST'])
@login_required
def password_user_change():
    current_pass = request.form.get('current_password')
    new_pass = request.form.get('new_password')
    confirm_pass = request.form.get('confirm_password')

    if new_pass == '' or confirm_pass == '' or current_pass == '':
       flash('Password field cannot be empty')
       return redirect(url_for('.get_password_page'))
    if new_pass == confirm_pass:
       if len(new_pass) < 7:
          flash('Password cannot be shorter than 7 characters')
          return redirect(url_for('.get_password_page'))
       try:
          user = change_password(current_user.id,current_pass,new_pass)
          if user:
           flash('Success')
          else:
            flash('Error')
       except Exception as e:
          flash(str(e))
    else:
       flash('New passwords do not match')
    return redirect(url_for('.get_password_page'))

@user_views.route('/users/assistant', methods=['POST'])
@login_required
@admin_only
def add_user_post():
    try:
      username = request.form.get('username')
      password = request.form.get('password')
      user = create_assistant(username,password)
      if user:
        flash('Success')
      else:
        flash('Error occurred')
    except:
      flash('Error occurred')
    return redirect(url_for('.assistant_management'))

@user_views.route('/users/manage', methods=['GET'])
@login_required
@admin_only
def assistant_management():
   assistants = get_all_assistant_by_offset(size,1)
   return render_template('manage_assistants.html',assistants = assistants['data'], current_page=1 , num_pages = assistants['num_pages'], previous = 1, next= 2)

@user_views.route('/users/manage/page/<offset>', methods=['GET'])
@login_required
@admin_only
def assistant_management_multi(offset):
   offset = int(offset)
   assistants = get_all_assistant_by_offset(size,offset)
   if offset - 1 <= 0:
        previous = 1
        offset = 1
   else:
        previous = offset - 1
   if offset + 1 >= assistants['num_pages']:
        next = assistants['num_pages']
   else:
        next = offset + 1
   return render_template('manage_assistants.html',assistants = assistants['data'], current_page=offset , num_pages = assistants['num_pages'], previous = previous, next= next)


@user_views.route('/users/assistant/<id>/reset', methods=['POST'])
@login_required
@admin_only
def assistant_password_reset(id):
   password = request.form.get('password')
   assistant = set_assistant_password(id,password)
   if not assistant:
      flash('Error occured')
   else:
      flash ('Success')
   return redirect(url_for('.assistant_management'))

@user_views.route('/users/assistant/<id>/delete', methods=['POST'])
@login_required
@admin_only
def assistant_delete(id):
   delete_assistant(id)
   return redirect(url_for('.assistant_management'))

@user_views.route('/api/users')
@login_required
@admin_only
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users')
@login_required
@admin_only
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/static/sw.js')
def sw_pwa():
  response = make_response(current_app.send_static_file('sw.js'))
  response.headers['Service-Worker-Allowed'] = '/'
  return response

@user_views.route('/loginpage',methods=['GET'])
def login_page():
  return render_template('index.html')

@user_views.route('/api/identify',methods=['GET'])  
def identify():
  if not current_user.is_anonymous:
        return jsonify(current_user.toJSON())
  return {}