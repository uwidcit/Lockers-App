from flask import Blueprint, redirect, render_template, request, send_from_directory

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')

@locker_views.route('/locker/add', methods=['POST'])
def create_new_locker():
    return {},200

@locker_views.route('/getLockers/available', methods=['GET'])
def get_available_lockers():
    return {},200

@locker_views.route('/getLockers/<id>', methods=['GET'])
def get_locker_id(id):
    return {},200

@locker_views.route('/getLockers/unavailable', methods=['GET'])
def get_unavailable_lockers():
    return {},200