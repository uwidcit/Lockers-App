from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    store_file,
    get_all_lockers
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/upload', methods=['POST'])
def upload_file_route():
    user_file = request.files.getlist('upload')

    for f in user_file:
        store_file(f)
    return []

@user_views.route('/users', methods=['GET'])
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

@user_views.route('/addpage',methods=['GET'])
def add_page():
  return render_template('add.html')

@user_views.route('/availpage',methods=['GET'])
def avail_page():
  return render_template('availability.html', results = get_all_lockers())

@user_views.route('/loginpage',methods=['GET'])
def login_page():
  return render_template('index.html')



@user_views.route('/removepage',methods=['GET'])
def remove_page():
  return render_template('remove.html')

