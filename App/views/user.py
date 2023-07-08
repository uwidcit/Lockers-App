from flask import Blueprint, render_template, jsonify, request, send_from_directory,send_file,current_app,make_response
from flask_login import login_required, current_user


from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    store_file,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/upload', methods=['POST'])
def upload_file_route():
    user_file = request.files.getlist('upload')

    for f in user_file:
        store_file(f)
    return []

@user_views.route('/users', methods=['GET'])
@login_required
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users')
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


@user_views.route('/removepage',methods=['GET'])
def remove_page():
  return render_template('remove.html')

@user_views.route('/api/identify',methods=['GET'])  
def identify():
  if not current_user.is_anonymous:
        return jsonify(current_user.toJSON())
  return {}