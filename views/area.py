from flask import Blueprint, redirect, render_template, request, send_from_directory

area_views = Blueprint('area_views', __name__, template_folder='../templates')

@area_views.route('/area/add', methods=['POST'])
def create_new_area():
    return {},200

@area_views.route('/get/area/all', methods=['GET'])
def get_all_areas():
    return {},200