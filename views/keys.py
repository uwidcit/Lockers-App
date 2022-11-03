from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify

from controllers import (
    add_new_key,
    get_all_keys,
)

keys_views = Blueprint('keys_views', __name__, template_folder='../templates')

@keys_views.route('/keys', methods=['GET'])
def key_page():
    
    return render_template('keys.html')

@keys_views.route('/key/add', methods=['POST'])
def create_new_key():
    key_id = request.json.get('key_id')
    key_1_status = request.json.get('key_1_status')
    key_2_status = request.json.get('key_2_status')

    newKey = add_new_key(key_id, key_1_status, key_2_status)

    if not newKey:
        return jsonify({"message":"Key alread exist or some error has occurred"}),400

    return jsonify({"data":newKey.toJSON()}),201
@keys_views.route('/get/keys/all',methods=['GET'])
def get_every_keys():
    return jsonify({"data":get_all_keys()}),200

@keys_views.route('/get/keys/available', methods=['GET'])
def get_available_keys():
    return {},200

@keys_views.route('/get/key/<id>', methods=['GET'])
def get_key_id(id):
    return {}

@keys_views.route('/getkeys/unavailable', methods=['GET'])
def get_unavailable_keys():
    return {}