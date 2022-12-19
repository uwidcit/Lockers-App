from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify

from controllers import (
    get_All_rentType
)

from forms import RentTypeAdd
rentType_views = Blueprint('rentType_views', __name__, template_folder='../templates')

@rentType_views.route('/rentType',methods=['GET'])
def render_rentType_new():
    return render_template('rentType.html',form = RentTypeAdd())

@rentType_views.route('/rentType/manage',methods=['GET'])
def render_rentType_all():
    return render_template('rentType_manage.html', results=get_All_rentType())