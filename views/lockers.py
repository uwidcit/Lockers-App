from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify

from controllers import (
    add_new_locker,
    get_lockers_available,
    get_lockers_unavailable,
    get_locker_id,
    get_all_lockers,
)

locker_views = Blueprint('locker_views', __name__, template_folder='../templates')


@locker_views.route('/locker', methods=['GET'])
def return_locker_page():
    form = Add()
    return render_template('locker.html',form=form)

@locker_views.route('/locker/add', methods=['POST'])
def create_new_locker():
    form = Add() # create form object
    if form.validate_on_submit():
        data = request.form # get data from form submission
        new_locker = add_new_locker(locker_code=data['locker_code'], area=data['area'], locker_type=data['locker_type'], staus=data['staus'], key_id=data['key_id'])



    if not new_locker:
        return jsonify({"message":"Locker already exist or some error has occurred"}),400

    return jsonify({"data":new_locker.toJSON()}),201

@locker_views.route('/lockers/get/available', methods=['GET'])
def get_available_lockers():
    locker_list = get_lockers_available()

    if not locker_list:
        return jsonify({"message":"No available lockers"}),200

    return jsonify({"data":locker_list}),200

@locker_views.route('/lockers/get/<id>', methods=['GET'])
def get_id_locker(id):
    locker = get_locker_id(id)

    if not locker:
        return jsonify({"message":"Locker not found"}),404

    return jsonify({"data":locker.toJSON()}),200

@locker_views.route('/lockers/get/all',methods=['GET'])
def return_all_lockers():
    locker_list = get_all_lockers()
    if not locker_list:
        return jsonify({"error":"No lockers available"}),404
    return jsonify({"data":locker_list}),200


@locker_views.route('/lockers/get/unavailable', methods=['GET'])
def get_unavailable_lockers():
    locker_list = get_lockers_unavailable()

    if not locker_list:
        return jsonify({"message":"No unavailable lockers"}),200

    return jsonify({"data":locker_list}),200