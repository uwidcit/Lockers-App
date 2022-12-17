from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify

from controllers import (
    get_area_all,
    get_area_by_id,
    add_new_area,
    delete_area,
    set_description,
    set_latitude,
    set_longitude,
)

area_views = Blueprint('area_views', __name__, template_folder='../templates')

@area_views.route('/area', methods=['POST'])
def create_new_area():
    locker_id = request.json.get('locker_id')
    description = request.json.get('description')
    longitude = request.json.get('longitiude')
    latitude = request.json.get('latitude')

    new_area = add_new_area(locker_id,description,longitude,latitude)

    if not new_area:
        return jsonify({"Message": "Area not created"}),400
    return jsonify(new_area.toJSON()),201

@area_views.route('/area', methods=['GET'])
def get_all_areas():
    return jsonify(get_area_all()),200

@area_views.route('/area/<id>', methods=['GET'])
def get_area_id(id):
    area = get_area_by_id(id)
    if not area:
        return jsonify({"Message": "Area not found"}),404
    return jsonify(area),200

@area_views.route('/area/<id>', methods=['DELETE'])
def remove_area(id):
    area = delete_area(id)

    if not area:
        return jsonify({"Message": "Area not deleted"}),400

    return jsonify({"Message": "Area deleted"}),200

@area_views.route('/area/<id>', methods=['PUT'])
def update_area(id):

    description = request.json.get('description')
    longitude = request.json.get('longitiude')
    latitude = request.json.get('latitude')

    if not set_description(id,description):
        return jsonify({"Message": "Error in processing description"}),400
    if not set_longitude (id, longitude):
        return jsonify({"Message": "Error in processing longitude"}),400
    if not set_latitude (id,latitude):
        return jsonify({"Message": "Error in processing latitude"}),400
    area = get_area_by_id(id)
    return jsonify(area.toJSON()),200