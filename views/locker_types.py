from flask import Blueprint, redirect, render_template, request, send_from_directory

locker_types_views = Blueprint('locker_types_views', __name__, template_folder='../templates')

@locker_types_views.route('/locker_types/add', methods=['POST'])
def create_new_locker_type():
    return {},200

@locker_types_views.route('/get/locker_type/<id>', methods=['GET'])
def get_locker_type_id(id):
    return {},200

@locker_types_views.route('/get/locker_types/all', methods=['GET'])
def get_all_locker_types():
    return {},200