from flask import Blueprint, redirect, render_template, request, send_from_directory,flash,url_for
from controllers import get_current_user
report_views = Blueprint('report_views', __name__, template_folder='../templates')

from controllers import (
    get_all_lockers,


)

@report_views.route('/report', methods=['GET'])
def report_page():
    return render_template('report.html')

@report_views.route('/report/transactions', methods=['POST'])
def report_page():
    return render_template('report.html')